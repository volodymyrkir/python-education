"""This module serves to load last 3 month`s tmdb data to minio"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from python_jobs.load_data_demand import push_all_movies_minio_job
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

with DAG("push_movies_3_month",
         default_args=default_args,
         schedule_interval=None,
         catchup=False
         ) as dag:
    task1 = PythonOperator(
        task_id="push_full_movies_minio", python_callable=push_all_movies_minio_job
    )
