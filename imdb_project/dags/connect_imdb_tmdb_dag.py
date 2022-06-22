"""This module provides dag for connecting tmdb and imdb data"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from spark_jobs.join_imdb_tmdb_data import join_imdb_tmdb_data


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

with DAG("connect_database_dag",
         default_args=default_args,
         schedule_interval='0 1 * * *',
         catchup=False) as dag_join:
    task1 = PythonOperator(
        task_id="fetch_minio_connect_postgres",
        python_callable=join_imdb_tmdb_data
    )
    wait_tmdb_data = ExternalTaskSensor(
        task_id='dag_push_postgres_sensor',
        poke_interval=20,
        timeout=180,
        soft_fail=False,
        retries=2,
        external_task_id='clear_fetched_raw_films',
        external_dag_id='push_movies_postgres',
        dag=dag_join)

wait_tmdb_data >> task1
