import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope='session', autouse=True)
def spark_session():
    """Fixture that enables SparkSession during tests run.

    Yields:
        SparkSession: current SparkSession
    """

    spark_session = SparkSession.builder.getOrCreate()
    spark_session.conf.set("spark.sql.session.timeZone", "UTC")

    yield spark_session

    spark_session.sparkContext.stop()
