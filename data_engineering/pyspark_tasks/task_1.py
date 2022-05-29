"""This module saves top 100 films according to IMDB ratings(all time,60th,last 10 years)"""
from pyspark import SparkConf
from pyspark.sql import SparkSession


def get_best_alltime(basics_df, ratings_df):
    return basics_df.join(ratings_df, basics_df['tconst'] == ratings_df['tconst'], 'inner') \
        .select(basics_df['tconst'], 'primaryTitle', 'numVotes', 'averageRating', 'startYear') \
        .where('numVotes>=100000 and titleType="movie"') \
        .orderBy('averageRating', ascending=False).limit(100)


def get_best_60th(basics_df,ratings_df):
    return basics_df.join(ratings_df, basics_df['tconst'] == ratings_df['tconst'], 'inner') \
        .select(basics_df['tconst'], 'primaryTitle', 'numVotes', 'averageRating', 'startYear') \
        .where('numVotes>=100000 and titleType="movie" and startYear between 1960 and 1969') \
        .orderBy('averageRating', ascending=False).limit(100)


def get_best_decade(basics_df,ratings_df):
    return basics_df.join(ratings_df, basics_df['tconst'] == ratings_df['tconst'], 'inner') \
        .select(basics_df['tconst'], 'primaryTitle', 'numVotes', 'averageRating', 'startYear') \
        .where('numVotes>=100000 and titleType="movie" and YEAR(current_date())-startYear<10') \
        .orderBy('averageRating', ascending=False).limit(100)


spark_session = (SparkSession.builder
                 .master('local')
                 .appName('task_1')
                 .config(conf=SparkConf())
                 .getOrCreate())


ratings_df_main = spark_session.read.csv(path='input/title.ratings.tsv.gz', sep='\t', header=True)
basics_df_main = spark_session.read.csv(path='input/title.basics.tsv.gz', sep='\t', header=True)

top_100_all = get_best_alltime(ratings_df_main,basics_df_main)

top_100_60th = get_best_60th(ratings_df_main, basics_df_main)

top_100_dec = get_best_decade(ratings_df_main, basics_df_main)

if __name__ == "__main__":

    top_100_all.write.csv(path='output/top_100_all')
    top_100_60th.write.csv(path='output/top_100_60th')
    top_100_dec.write.csv(path='output/top_100_dec')
