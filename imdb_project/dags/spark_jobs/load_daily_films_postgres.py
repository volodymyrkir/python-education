"""this module fetches json data from minio and pushes it to postgres db(also can clear raw data)"""
import os
from functools import reduce
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from dotenv import load_dotenv
import boto3

load_dotenv()
MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
USER_PG_DB = os.getenv('USER_PG_DB')


def get_spark_connection(app_name):
    """returns spark session and spark context objects"""
    config = SparkConf()
    spark_context = SparkContext(master="local[*]", appName=app_name)
    spark_session = (SparkSession.builder
                     .master('local')
                     .appName(app_name)
                     .config(conf=config)
                     .getOrCreate())
    return spark_session, spark_context


def get_minio_connection():
    """returns minio aws connection"""
    session = boto3.session.Session()

    s3 = session.resource('s3',
                          endpoint_url='http://s3:9000',
                          aws_access_key_id=MINIO_ROOT_USER,
                          aws_secret_access_key=MINIO_ROOT_PASSWORD,
                          region_name='us-east-1')
    return s3


def connect_to_postgres(user, password, host):
    """Connects to postgres server"""
    engine_postgres = create_engine(f'postgresql://{user}:{password}@{host}:5432').connect()
    return engine_postgres


def connect_to_postgres_db(user, password, host, database):
    """Connects to postgres db"""
    postgres_connection = connect_to_postgres(user, password, host)
    database_url = f'postgresql://{user}:{password}@{host}:5432/{database}'
    if not database_exists(database_url):
        postgres_connection.execution_options(isolation_level="AUTOCOMMIT").execute(
            f'create database {database}')
    engine_db_postgres = create_engine(f'postgresql://{user}:{password}@{host}:5432/{database}')
    postgres_connection.close()
    return engine_db_postgres


def fetch_json_files(s3, bucket_name: str = "raw-data"):
    """returns list of jsons in minio bucket"""
    json_bucket = s3.Bucket(bucket_name)
    list_of_jsons = []  # must be one file according to same schedule interval, but who knows :)
    for json_object in json_bucket.objects.all():
        if json_object.key.endswith('.json'):
            list_of_jsons.append(json_object.get()['Body'].read().decode('utf-8'))
    return list_of_jsons


def spark_concat_jsons(list_of_jsons, spark_session, spark_context):
    """Reduces list of jsons into single dataframe"""
    return (reduce(DataFrame.unionAll,
                   [spark_session.read.json
                    (spark_context.parallelize([json_object]))
                    for json_object in list_of_jsons])).dropDuplicates()


def spark_select_postgres_data(tmdb_dataframe_input):
    """Returns dataframe with necessary columns"""
    tmdb_dataframe_input = tmdb_dataframe_input. \
        withColumn('genre', tmdb_dataframe_input['genres'].getItem(0)['name'])
    return tmdb_dataframe_input. \
        select(f.col('id'), f.col('imdb_id'),
               f.col('genre'), f.col('runtime')).dropDuplicates(['id'])


def clear_data_json(**kwargs):
    """deletes raw data from bucket"""
    s3 = kwargs['s3']
    my_buck = s3.Bucket(kwargs['bucket_name'])
    for json_file in my_buck.objects.all():
        if json_file.key.endswith('.json'):
            s3.Object(kwargs['bucket_name'], json_file.key).delete()


def check_database_duplicates(connection, dataframe):
    """Checks, whether dataframe has duplicate values that are already in db"""
    cursor = connection.execute('SELECT DISTINCT(id) FROM film_tmdb_imdb')
    id_keys = cursor.fetchall()
    cursor.close()
    list_of_keys = [value_tuple[0] for value_tuple in id_keys]
    return dataframe.filter(~dataframe.id.isin(list_of_keys)).toPandas()


def prepare_tmdb_dataframe(bucket_name, spark_session, spark_context, s3):
    """Encapsulates logic, concerned with processing tmdb data"""
    json_list = fetch_json_files(s3, bucket_name)
    if not json_list:
        return None
    else:
        tmdb_dataframe = spark_concat_jsons(json_list, spark_session, spark_context)
        return spark_select_postgres_data(tmdb_dataframe)


def fetch_minio_push_postgres():
    """Main function of module, fetches jsons from minio,
     processes them and pushes into postgres db"""
    spark_session, spark_context = get_spark_connection('load_daily_films_postgres')
    s3_con = get_minio_connection()
    tmdb_dataframe = prepare_tmdb_dataframe('raw-data', spark_session, spark_context, s3_con)
    if tmdb_dataframe:
        with connect_to_postgres_db(POSTGRES_USER, POSTGRES_PASSWORD, 'database', USER_PG_DB).connect() \
                as tmdb_imdb_connection:
            tmdb_imdb_connection \
                .execute('CREATE TABLE IF NOT EXISTS film_tmdb_imdb'
                         '(id Integer PRIMARY KEY,imdb_id varchar NOT NULL,genre varchar,runtime integer)')
            tmdb_dataframe = check_database_duplicates(tmdb_imdb_connection, tmdb_dataframe)
            tmdb_dataframe.to_sql('film_tmdb_imdb',
                                  con=tmdb_imdb_connection, if_exists='append', index=False)
