import pytest
from pyspark.sql.types import Row
from equality import dfs_equal
from data_engineering.pyspark_tasks.task_1 import get_best_alltime, get_best_60th


@pytest.fixture()
def test_ratings_df(spark_session):
    return spark_session.createDataFrame([
        Row(tconst=1, numVotes=100001, averageRating=9.3),
        Row(tconst=2, numVotes=400000, averageRating=9.9),
        Row(tconst=3, numVotes=10000, averageRating=8.0),
        Row(tconst=4, numVotes=200000, averageRating=8.3),
        Row(tconst=5, numVotes=300000, averageRating=9.4)
    ])


def test_get_best_alltime(spark_session,test_ratings_df):
    test_basics_df = spark_session.createDataFrame([
        Row(tconst=1, titleType='movie',
            primaryTitle='first_movie', startYear=2003),
        Row(tconst=2, titleType='series',
            primaryTitle='first_series', startYear=2003),
        Row(tconst=3, titleType='movie',
            primaryTitle='second_movie', startYear=2004),
        Row(tconst=4, titleType='movie',
            primaryTitle='third_movie', startYear=2003),
        Row(tconst=5, titleType='movie',
            primaryTitle='fourth_movie', startYear=2020)
    ])

    actual_df = get_best_alltime(test_basics_df, test_ratings_df)

    expected_df = spark_session.createDataFrame([
        Row(tconst=1, primaryTitle='first_movie', numVotes=100001, averageRating=9.3, startYear=2003),
        Row(tconst=5, primaryTitle='fourth_movie', numVotes=300000, averageRating=9.4, startYear=2020),
        Row(tconst=4, primaryTitle='third_movie', numVotes=200000, averageRating=8.3, startYear=2003)
    ])

    assert dfs_equal(actual=actual_df, expected=expected_df)


def test_get_best_60th(spark_session,test_ratings_df):
    test_basics_df = spark_session.createDataFrame([
        Row(tconst=1, titleType='movie',
            primaryTitle='first_movie', startYear=1969),
        Row(tconst=2, titleType='series',
            primaryTitle='first_series', startYear=2003),
        Row(tconst=3, titleType='movie',
            primaryTitle='second_movie', startYear=1961),
        Row(tconst=4, titleType='movie',
            primaryTitle='third_movie', startYear=1960),
        Row(tconst=5, titleType='movie',
            primaryTitle='fourth_movie', startYear=2020)
    ])

    actual_df = get_best_60th(test_basics_df, test_ratings_df)

    expected_df = spark_session.createDataFrame([
        Row(tconst=1, primaryTitle='first_movie', numVotes=100001, averageRating=9.3, startYear=1969),
        Row(tconst=4, primaryTitle='third_movie', numVotes=200000, averageRating=8.3, startYear=1960)
    ])

    assert dfs_equal(actual=actual_df, expected=expected_df)
