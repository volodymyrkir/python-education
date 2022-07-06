"""this module serves for scheduling worflow for processing data from various api`s of different crypto markets"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from spark_jobs.collect_currencies import push_bitmex_json, push_poloniex_json, push_bitfinex_json

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2021, 1, 1, 0, 0, 0),
    "email": ["my_email@mail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1)
}


with DAG("push_json_minio", default_args=default_args, schedule_interval='* * * * *', catchup=False) as dag:
    task1 = PythonOperator(
        task_id="push_bitfinex_minio", python_callable=push_bitfinex_json
    )

    task2 = PythonOperator(
        task_id="push_bitmex_minio", python_callable=push_bitmex_json
    )

    task3 = PythonOperator(
        task_id="push_poloniex_minio", python_callable=push_poloniex_json
    )

