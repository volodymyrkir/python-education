"""this module serves for scheduling worflow for processing data from various api`s of different crypto markets"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from spark_jobs.send_parquet import push_parquet_bitfinex, push_parquet_bitmex, push_parquet_poloniex

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2021, 1, 2, 0, 0, 0),
    "email": ["my_email@mail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1)
}

with DAG("push_stats_minio", default_args=default_args, schedule_interval='40 * * * *', catchup=False) as dag:
    task1 = PythonOperator(
        task_id="get_stat_bitfinex", python_callable=push_parquet_bitfinex
    )

    task2 = PythonOperator(
        task_id="get_stat_bitmex", python_callable=push_parquet_bitmex
    )

    task3 = PythonOperator(
        task_id="get_stat_poloniex", python_callable=push_parquet_poloniex
    )
