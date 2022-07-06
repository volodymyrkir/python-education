"""This module saves top 100 films according to IMDB ratings(all time,60th,last 10 years)"""
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


def get_best_alltime(basics_df, ratings_df):
    return (basics_df.join(ratings_df, basics_df['tconst'] == ratings_df['tconst'], 'inner')
            .select(basics_df['tconst'], 'primaryTitle', 'numVotes', 'averageRating', 'startYear')
            .where((f.col('numVotes') >= 100_000) & (f.col('titleType') == 'movie'))
            .orderBy('averageRating', ascending=False).limit(100))


def get_best_60th(basics_df, ratings_df):
    return (basics_df.join(ratings_df, basics_df['tconst'] == ratings_df['tconst'], 'inner')
            .select(basics_df['tconst'], 'primaryTitle', 'numVotes', 'averageRating', 'startYear')
            .where((f.col('numVotes') >= 100_000) & (f.col('titleType') == 'movie') &
                   f.col('startYear').between(1960, 1969))
            .orderBy('averageRating', ascending=False).limit(100))


def get_best_decade(basics_df, ratings_df):
    return (basics_df.join(ratings_df, basics_df['tconst'] == ratings_df['tconst'], 'inner')
            .select(basics_df['tconst'], 'primaryTitle', 'numVotes', 'averageRating', 'startYear')
            .where((f.col('numVotes') >= 100_000) & (f.col('titleType') == 'movie')
                   & ((f.year(f.current_date()) - f.col('startYear')) < 10))
            .orderBy('averageRating', ascending=False).limit(100))


def get_raw_input():
    ratings_df_main = spark_session.read.csv(path='input/title.ratings.tsv.gz', sep='\t', header=True)
    basics_df_main = spark_session.read.csv(path='input/title.basics.tsv.gz', sep='\t', header=True)
    return ratings_df_main, basics_df_main


spark_session = (SparkSession.builder
                 .master('local')
                 .appName('task_1')
                 .config(conf=SparkConf())
                 .getOrCreate())

if __name__ == "__main__":
    raw_data = get_raw_input()
    top_100_all = get_best_alltime(*raw_data)

    top_100_60th = get_best_60th(*raw_data)

    top_100_dec = get_best_decade(*raw_data)

    top_100_all.write.csv(path='output/top_100_all')
    top_100_60th.write.csv(path='output/top_100_60th')
    top_100_dec.write.csv(path='output/top_100_dec')
