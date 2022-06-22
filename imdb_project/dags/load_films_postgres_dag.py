"""This module serves for loading data from minio to postgres db"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from spark_jobs.load_daily_films_postgres import fetch_minio_push_postgres, clear_data_json, get_minio_connection


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
with DAG("push_movies_postgres", default_args=default_args, schedule_interval='0 1 * * *', catchup=False) as dag:
    task1 = PythonOperator(
        task_id="fetch_films_minio_push_postgres",
        python_callable=fetch_minio_push_postgres
    )
    task2 = PythonOperator(
        task_id="clear_fetched_raw_films",
        python_callable=clear_data_json,
        op_kwargs={'bucket_name': 'raw-data', 's3': get_minio_connection()}
    )
    wait_hourly_task = ExternalTaskSensor(
        task_id='push_last_movies_sensor',
        poke_interval=20,
        timeout=180,
        soft_fail=False,
        retries=2,
        external_task_id='push_last_movies_minio',
        external_dag_id='push_last_day_movies',
        dag=dag)

wait_hourly_task >> task1 >> task2
