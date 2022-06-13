"""This module saves csv file with top-10 films for each category"""
from pyspark import SparkConf
from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from pyspark.sql import Window as w


def get_top10_category(basics_df, ratings_df):
    """returns data frame with films grouped by category, 10 for each category"""
    window = w.partitionBy('genres').orderBy(f.col('averageRating').desc())

    res_unprepared = (basics_df
                      .join(ratings_df, basics_df['tconst'] == ratings_df['tconst'], 'inner')
                      .select(basics_df['tconst'], 'primaryTitle',
                              'genres', 'numVotes', 'averageRating', 'startYear')
                      .where(f.col('numVotes') > 100_000)
                      .orderBy(f.col('averageRating').asc()))

    return (res_unprepared.withColumn("Rank within category", f.row_number().over(window))
            .filter(f.col("Rank within category") <= 10))


def replace_null(column, value):
    """replaces nulls in column(used in title.basics.tsv.gz"""
    return f.when(column != value, column).otherwise(f.lit(None))


def main():
    """main function of the module"""
    spark_session = (SparkSession.builder
                     .master('local')
                     .appName('task_2')
                     .config(conf=SparkConf())
                     .getOrCreate())

    basics_df_main = spark_session.read.csv(path='input/title.basics.tsv.gz', sep='\t', header=True, nullValue=None)
    basics_df_main = basics_df_main.filter(basics_df_main.titleType == 'movie')
    basics_df_main = basics_df_main.withColumn("genres", replace_null(f.col('genres'), '\\N'))

    ratings_df_main = (spark_session.read
                       .csv(path='input/title.ratings.tsv.gz', sep='\t', header=True))

    res = get_top10_category(basics_df_main, ratings_df_main)
    return res



if __name__ == "__main__":
    top_10_category = main()
    (top_10_category.coalesce(1)
     .write.format("com.databricks.spark.csv")
     .option("header", "true")
     .save("output/top_10_by_category.csv"))
