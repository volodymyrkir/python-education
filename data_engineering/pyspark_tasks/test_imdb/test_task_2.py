import pytest
import pyspark.sql.functions as f
import pyspark.sql.types as t
from pyspark.sql.types import Row
from equality import dfs_equal
from data_engineering.pyspark_tasks.task_2 import replace_null, get_top10_category


@pytest.fixture()
def test_ratings_df(spark_session):
    return spark_session.createDataFrame([
        Row(tconst=1, numVotes=100001, averageRating=9.3),
        Row(tconst=2, numVotes=400000, averageRating=9.9),
        Row(tconst=3, numVotes=10000, averageRating=8.0),
        Row(tconst=4, numVotes=200000, averageRating=8.3),
        Row(tconst=5, numVotes=300000, averageRating=9.4)
    ])


def test_replace_null(spark_session):
    test_frame = spark_session.createDataFrame([
        Row(id=2, some_val='some_res'),
        Row(id=1, some_val='\\N')
    ])
    actual_df = test_frame.withColumn('some_val', replace_null(f.col('some_val'), '\\N'))
    expected_df = spark_session.createDataFrame([
        Row(id=2, some_val='some_res'),
        Row(id=1, some_val=None)
    ])
    assert dfs_equal(actual_df, expected_df)


def test_get_top10_category(spark_session, test_ratings_df):
    test_basics_df = spark_session.createDataFrame([
        Row(tconst=1, titleType='movie',
            primaryTitle='first_movie', genres='horror', startYear=2003),
        Row(tconst=2, titleType='movie',
            primaryTitle='first_add_movie', genres='horror', startYear=2003),
        Row(tconst=3, titleType='movie',
            primaryTitle='second_movie', genres='western', startYear=2004),
        Row(tconst=4, titleType='movie',
            primaryTitle='third_movie', genres='comedy', startYear=2003),
        Row(tconst=5, titleType='movie',
            primaryTitle='fourth_movie', genres='sitcom', startYear=2020)
    ])
    actual_df = get_top10_category(test_basics_df, test_ratings_df)
    schema_df = t.StructType()
    schema_df.add("tconst", t.LongType(), True)
    schema_df.add("primaryTitle", "string", True)
    schema_df.add("genres", "string", True)
    schema_df.add("numVotes", t.LongType(), True)
    schema_df.add("averageRating", "double", True)
    schema_df.add("startYear", t.LongType(), True)
    schema_df.add("rank_within_category", t.IntegerType(), True)
    expected_df = spark_session.createDataFrame([
        Row(tconst=4, primaryTitle='third_movie',
            genres='comedy', numVotes=200000, averageRating=8.3, startYear=2003, rank_within_category=1),
        Row(tconst=2, primaryTitle='first_add_movie',
            genres='horror', numVotes=400000, averageRating=9.9, startYear=2003, rank_within_category=1),
        Row(tconst=1, primaryTitle='first_movie',
            genres='horror', numVotes=100001, averageRating=9.3, startYear=2003, rank_within_category=2),
        Row(tconst=5, primaryTitle='fourth_movie',
            genres='sitcom', numVotes=300000, averageRating=9.4, startYear=2020, rank_within_category=1)
    ], schema=schema_df)
    assert dfs_equal(actual_df, expected_df)
