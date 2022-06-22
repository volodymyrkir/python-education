"""This module serves for saving latest movies of previous day to minio storage"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .load_data_demand import get_json_set, push_json_minio


def load_latest_movies_minio():
    """loads previous day films to minio storage"""
    previous_day_date = (datetime.now()-relativedelta(days=1)).strftime('%Y-%m-%d')
    json_object = get_json_set(previous_day_date, previous_day_date)
    push_json_minio('raw-data', json_object)
