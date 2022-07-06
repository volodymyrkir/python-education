"""This module joins tmdb data from postgres db and imdb data from minio"""
import os
import pandas as pd
from .load_daily_films_postgres import get_minio_connection, connect_to_postgres_db


POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
USER_PG_DB = os.environ.get('USER_PG_DB')


def get_title_basics_dataframe(bucket_name, s3):
    """returns basics imdb dataframe"""
    imdb_tsv_object = s3.Object(bucket_name=bucket_name, key='title.ratings.tsv.gz')
    df = pd.read_csv(imdb_tsv_object.get()['Body'], compression='gzip', header=0, sep='\t', )
    return df


def join_imdb_tmdb_data():
    """Joins tmdb and imdb data"""
    s3 = get_minio_connection()
    with connect_to_postgres_db(POSTGRES_USER, POSTGRES_PASSWORD, 'database', USER_PG_DB).connect()\
            as tmdb_imdb_db:
        imdb_dataframe = get_title_basics_dataframe('ratings-bucket', s3)
        imdb_dataframe.to_sql('imdb_table', con=tmdb_imdb_db, if_exists='replace', index=False)
        tmdb_imdb_db\
            .execute('ALTER TABLE film_tmdb_imdb ADD COLUMN IF NOT EXISTS average_rating double precision')
        tmdb_imdb_db\
            .execute('ALTER TABLE film_tmdb_imdb ADD COLUMN IF NOT EXISTS num_votes bigint')
        tmdb_imdb_db.execute('UPDATE film_tmdb_imdb set'
                             ' average_rating=imdb_table."averageRating",num_votes=imdb_table."numVotes"'
                             ' from imdb_table  where imdb_id = imdb_table.tconst')
        tmdb_imdb_db.execute('TRUNCATE TABLE imdb_table')
