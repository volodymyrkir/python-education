"""This module serves for loading previous day tmdb data into minio storage"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from python_jobs.load_latest_movies import load_latest_movies_minio

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

with DAG("push_last_day_movies", default_args=default_args, schedule_interval='0 1 * * *', catchup=False) as dag:
    task1 = PythonOperator(
        task_id="push_last_movies_minio", python_callable=load_latest_movies_minio
    )
