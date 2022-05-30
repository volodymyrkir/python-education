"""This module saves data frame with top 10 films by each category on each decade"""
from pyspark import SparkConf
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from pyspark.sql import Window as w
from task_2 import replace_null


def get_top10_decade(basics_df, ratings_df):
    """Returns data frame with top 10 films for each category for each decade"""
    res_unprepared = basics_df \
        .join(ratings_df, basics_df['tconst'] == ratings_df['tconst'], 'inner') \
        .select(basics_df['tconst'], 'primaryTitle',
                'genres', 'numVotes', 'averageRating', 'startYear') \
        .where('numVotes>=100000') \
        .orderBy(f.col('averageRating').asc())
    res_unprepared = res_unprepared.withColumn("decade",
                                               f.concat_ws
                                               ('-', f.floor(f.year('startYear') / 10) * 10,
                                                f.floor(f.year('startYear') / 10) * 10 + 9))
    films_50th = res_unprepared.select('*').filter(res_unprepared.startYear >= 1950)
    window = w.partitionBy('genres', 'decade').orderBy(f.col('averageRating').desc())
    return films_50th.withColumn("Rank within category", f.row_number().over(window)) \
        .filter(f.col("Rank within category") <= 10) \
        .orderBy(f.col('decade').desc(), f.col('genres').desc())


def main():
    """main function of the module"""
    spark_session = (SparkSession.builder
                     .master('local')
                     .appName('task_3')
                     .config(conf=SparkConf())
                     .getOrCreate())

    basics_df_main = spark_session.read.csv(path='input/title.basics.tsv.gz', sep='\t', header=True)
    basics_df_main = basics_df_main.filter(basics_df_main.titleType == 'movie')
    basics_df_main = basics_df_main.withColumn("genres", replace_null(f.col('genres'), '\\N'))

    ratings_df_main = spark_session.read \
        .csv(path='input/title.ratings.tsv.gz', sep='\t', header=True)

    res = get_top10_decade(basics_df_main, ratings_df_main)
    return res


top_10_decade = main()

if __name__ == "__main__":
    top_10_decade.coalesce(1) \
        .write.format("com.databricks.spark.csv") \
        .option("header", "true") \
        .save("output/top_10_decade_and_category.csv")
