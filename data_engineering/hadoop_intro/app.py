from pyspark.sql import SparkSession


def main():
    spark = (SparkSession
             .builder
             .appName('Simple Example')
             .getOrCreate())

    (spark
     .read.csv('hdfs://namenode:9000/daily_weather_2020.csv',
               header=True)
     .groupby('Country/Region', 'icon').count()
     .coalesce(1)
     .write.csv('hdfs://namenode:9000/daily_weather_2020_by_country/',
                header=True, mode='overwrite'))


if __name__ == '__main__':
    main()
