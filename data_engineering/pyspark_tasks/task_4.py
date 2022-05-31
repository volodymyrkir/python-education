from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from task_1 import top_100_all


def get_actors_squad(actors_df, best_actors_df):
    return best_actors_df.join(actors_df, actors_df['nconst'] == best_actors_df['nconst']) \
        .select(actors_df.nconst, actors_df.primaryName).limit(10)


def get_best_actors(actors_raw_df, top_100_actors):
    actors_raw_df = actors_raw_df.where(f.col('category').like("%actor%"))
    best_actors = top_100_actors.join(actors_raw_df, top_100_all['tconst'] == actors_raw_df['tconst'])
    best_actors = best_actors \
        .groupBy('nconst') \
        .agg(f.count('primaryTitle').alias('films_total')) \
        .orderBy('films_total') \
        .filter(f.col('films_total') > 1)
    return best_actors


def main():
    spark_session = (SparkSession.builder
                     .master('local')
                     .appName('task_4')
                     .config(conf=SparkConf())
                     .getOrCreate())
    actors_raw_df = spark_session.read.csv(path='input/title.principals.tsv.gz', sep='\t', header=True)
    best_ac = get_best_actors(actors_raw_df, top_100_all)

    actors_names_df = spark_session.read.csv(path='input/name.basics.tsv.gz', sep='\t', header=True)
    actors_alive_df = actors_names_df.filter(f.col('deathYear') == '\\N')

    actors_squad = get_actors_squad(actors_alive_df, best_ac)
    return actors_squad


actors_squad_df = main()

if __name__ == "__main__":
    actors_squad_df.coalesce(1) \
        .write.format("com.databricks.spark.csv") \
        .option("header", "true") \
        .save("output/actors_squad.csv")
