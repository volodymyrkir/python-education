from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import Window as w
import pyspark.sql.functions as f


def get_directors(crew_raw_df):
    crew_array_df = (crew_raw_df.select(crew_raw_df.tconst, f.split(f.col("directors"), ",").alias("directors_array"))
        .drop("directors"))
    directors_codes = crew_array_df.select(f.col('tconst').alias('movie_code'), f.explode('directors_array')
                                           .alias('director_code'))
    directors_codes = directors_codes.where(f.col('director_code') != '\\N')
    return directors_codes


def get_movies(titles_raw_df):
    movies = titles_raw_df.filter(titles_raw_df['titleType'] == 'movie')
    return movies


def get_directors_movies(movies_raw_df, directors_codes):
    return movies_raw_df.join(directors_codes, movies_raw_df['tconst'] == directors_codes['movie_code'])


def get_popular_movies(director_movie_df, ratings_df):
    director_movie_popularity = (director_movie_df.join(ratings_df,
                                                        director_movie_df['tconst'] == ratings_df['tconst'])
                                 .drop('movie_code'))
    window = w.partitionBy('director_code').orderBy(f.col('averageRating').desc())
    director_movie_popularity = (director_movie_popularity.withColumn("movie_rank", f.row_number().over(window))
                                 .filter(f.col("movie_rank") <= 5))
    return director_movie_popularity


def get_names_directors(staff_raw_df, most_popular_movies):
    directors_names = most_popular_movies.join(staff_raw_df,
                                               staff_raw_df.nconst == most_popular_movies.director_code)
    top_movies_director = directors_names.select('primaryName', 'primaryTitle', 'startYear', 'averageRating',
                                                 'numVotes')
    return top_movies_director


def main():
    spark_session = (SparkSession.builder
                     .master('local')
                     .appName('task_5')
                     .config(conf=SparkConf())
                     .getOrCreate())
    crew_df = spark_session.read.csv(path='input/title.crew.tsv.gz', sep='\t', header=True)
    staff_df = spark_session.read.csv(path='input/name.basics.tsv.gz', sep='\t', header=True)
    ratings_df = (spark_session.read
                  .csv(path='input/title.ratings.tsv.gz', sep='\t', header=True))
    titles_df = spark_session.read.csv(path='input/title.basics.tsv.gz', sep='\t', header=True)

    directors_codes_df = get_directors(crew_df)

    movies_df = get_movies(titles_df)

    director_movie_df = get_directors_movies(movies_df, directors_codes_df)

    most_popular_movies = get_popular_movies(director_movie_df, ratings_df)

    movies_director_names = get_names_directors(staff_df, most_popular_movies)

    return movies_director_names


if __name__ == "__main__":
    best_movies_directors = main()
    (best_movies_directors.coalesce(1)
     .write.format("com.databricks.spark.csv")
     .option("header", "true")
     .save("output/best_movies_by_directors.csv"))
