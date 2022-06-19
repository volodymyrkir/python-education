"""This module serves for saving last 3 month`s films to minio storage"""
import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
import requests
import boto3

load_dotenv()
MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
API_KEY = 'a76a378f657bde880c649956809cb6c6'
session = boto3.session.Session()
s3 = session.resource('s3',
                      endpoint_url='http://s3:9000',
                      aws_access_key_id=MINIO_ROOT_USER,
                      aws_secret_access_key=MINIO_ROOT_PASSWORD,
                      region_name='us-east-1')
headers = CaseInsensitiveDict()
headers["Connection"] = "keep-alive"
headers["Keep-Alive"] = "timeout=10, max=501"

requests_session = requests.Session()


def get_film_data(tmdb_id):
    """returns imdb film data"""
    return requests_session.get(f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}',
                                headers=headers).json()


def iterate_over_page(page, result_film_set):
    """Iterates over page in search of imdb films"""
    for film in page['results']:
        full_film_data = get_film_data(film['id'])
        if not full_film_data['imdb_id'] is None:
            result_film_set.append(full_film_data)


def get_json_set(left_border, right_border):
    """collects json file that consists of films"""

    main_link = (f'https://api.themoviedb.org/3/discover/movie?'
                 f'api_key={API_KEY}&'
                 f'primary_release_date.gte={left_border}&'
                 f'primary_release_date.lte={right_border}')

    result_film_set = []
    main_page = requests_session.get(main_link, headers=headers).json()
    iterate_over_page(main_page, result_film_set)
    last_page_num = main_page["total_pages"] + 1 if main_page["total_pages"] <= 500 else 501
    for page_num in range(2, last_page_num):
        page = requests_session.get(main_link + f'&page={page_num}', headers=headers).json()
        iterate_over_page(page, result_film_set)
    json_object = json.dumps(result_film_set)
    return json_object


def push_json_minio(bucket_name, json_object):
    """pushes imdb films to minio storage"""
    if not s3.Bucket(bucket_name) in s3.buckets.all():
        s3.create_bucket(Bucket=bucket_name)
    s3.Bucket(bucket_name).put_object(
        Key=f'{bucket_name}-{datetime.now()}.json',
        Body=json_object
    )


def push_all_movies_minio_job():
    """Pushes collected from api jsons to minio storage"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    three_month_back = (datetime.now() - relativedelta(months=3)).strftime('%Y-%m-%d')
    json_object = get_json_set(left_border=three_month_back, right_border=current_date)
    requests_session.close()
    push_json_minio('raw-data', json_object)
