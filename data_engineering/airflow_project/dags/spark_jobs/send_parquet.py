"""This module serves for sending parquet files to minio storage using raw json data"""
from datetime import datetime
from functools import reduce
from io import BytesIO
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import functions as f
from pyspark.sql import DataFrame
import boto3
import pyarrow

conf = SparkConf()
spark_context = SparkContext(master="local[*]", appName="collect_currencies")
spark_session = (SparkSession.builder
                 .master('local')
                 .appName('collect_currencies')
                 .config(conf=conf)
                 .getOrCreate())

session = boto3.session.Session()

s3 = session.resource('s3',
                      endpoint_url='http://s3:9000',
                      aws_access_key_id='minio_access_key',
                      aws_secret_access_key='minio_secret_key',
                      region_name='us-east-1')


def fetch_data_json(bucket_name):
    """fetches all json raw data from particular bucket"""
    json_objects = []
    my_buck = s3.Bucket(bucket_name)
    for json_file in my_buck.objects.all():
        if json_file.key.endswith('.json'):
            json_objects.append(json_file.get()['Body'].read().decode('utf-8'))
    return json_objects


def clear_data_json(boto_resource, bucket_name):
    """deletes raw data from bucket"""
    my_buck = boto_resource.Bucket(bucket_name)
    for json_file in my_buck.objects.all():
        if json_file.key.endswith('.json'):
            s3.Object(bucket_name, json_file.key).delete()


def spark_concat_jsons(bucket_name):
    """gets json list concatenated to single data frame"""
    jsons = fetch_data_json(bucket_name)
    return reduce(DataFrame.unionAll,
                  [spark_session.read.json(spark_context.parallelize([file])) for file in jsons])


def process_bitfinex_df():
    """processes bitfinex data frame to correct format"""
    bitfinex_df = spark_concat_jsons('bitfinex')
    bitfinex_df = bitfinex_df.select(f.col('exchange').alias('market_name'),
                                     f.to_timestamp(f.col('timestamp')).alias('datetime'),
                                     f.col('type').alias('transaction_type'),
                                     f.col('amount').alias('bitcoin_amount'),
                                     f.round(f.col('price'), 3).alias('price'))
    return bitfinex_df


def process_bitmex_df():
    """processes bitmex data frame to correct format"""
    bitmex_df = spark_concat_jsons('bitmex')
    bitmex_df = bitmex_df.withColumn('market_name', f.lit('bitmex'))
    bitmex_df = bitmex_df.select(f.col('market_name'),
                                 f.date_trunc("second",
                                              f.to_timestamp(f.col('timestamp'))).alias('datetime'),
                                 f.lower(f.col('side')).alias('transaction_type'),
                                 f.col('homeNotional').alias('bitcoin_amount'),
                                 f.round(f.col('price'), 3).alias('price'))
    return bitmex_df


def process_poloniex_df():
    """processes poloniex data frame to correct format"""
    poloniex_df = spark_concat_jsons('poloniex')
    poloniex_df = poloniex_df.withColumn('market_name', f.lit('poloniex'))
    poloniex_df = poloniex_df.select(f.col('market_name'),
                                     f.to_timestamp(f.col('date')).alias('datetime'),
                                     f.lower(f.col('type')).alias('transaction_type'),
                                     f.col('amount').alias('bitcoin_amount'),
                                     f.round(f.col('rate'), 3).alias('price'))
    return poloniex_df


def save_dataframe_to_parquet(dataframe, boto_resource, bucket):
    """saves data frame in parquet format to s3 bucket"""
    if not s3.Bucket(f'{bucket}-parquet') in s3.buckets.all():
        s3.create_bucket(Bucket=f'{bucket}-parquet')
    with BytesIO() as byte_buffer:
        dataframe.toPandas().to_parquet(byte_buffer, index=False)
        boto_resource.Bucket(f"{bucket}-parquet").put_object(
            Key=f'{bucket}-{datetime.now()}.parquet',
            Body=byte_buffer.getvalue()
        )


def push_parquet_bitfinex():
    """Main function for bitfinex bucket to save data in parquet"""
    bitfinex_df = process_bitfinex_df()
    save_dataframe_to_parquet(bitfinex_df, s3, 'bitfinex')
    clear_data_json(s3, 'bitfinex')


def push_parquet_bitmex():
    """Main function for bitmex bucket to save data in parquet"""
    bitmex_df = process_bitmex_df()
    save_dataframe_to_parquet(bitmex_df, s3, 'bitmex')
    clear_data_json(s3, 'bitmex')


def push_parquet_poloniex():
    """Main function for poloniex bucket to save data in parquet"""
    poloniex_df = process_poloniex_df()
    save_dataframe_to_parquet(poloniex_df, s3, 'poloniex')
    clear_data_json(s3, 'poloniex')
