"""This module serves for getting data frame from crypto markets` API`s"""
import json
import time
from datetime import datetime, timedelta
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark import SparkContext
import boto3
import requests

services = {
    'bitfinex': 'https://api.bitfinex.com/v1/trades/btcusd?',
    'bitmex': 'https://www.bitmex.com/api/v1/trade?symbol=XBTUSD&',
    'poloniex': 'https://poloniex.com/public?command=returnTradeHistory&currencyPair=USDT_BTC&',
}
conf = SparkConf()
spark_context = SparkContext(master="local[*]", appName="collect_currencies")
spark_session = (SparkSession.builder
                 .master('local')
                 .appName('collect_currencies')
                 .config(conf=conf)
                 .getOrCreate())

session = boto3.session.Session()

s3 = session.resource('s3',
                      endpoint_url='http://s3:9000',
                      aws_access_key_id='minio_access_key',
                      aws_secret_access_key='minio_secret_key',
                      region_name='us-east-1')


def get_json_api(api_link):
    """Returns json in byte representation"""
    response = requests.get(api_link)
    if response.status_code == 200:
        return bytes(json.dumps(response.json(),
                                indent=2), encoding="utf-8")
    return None


def push_bitfinex_json():
    """pushes bitfinex json raw data"""
    now = int(time.mktime(datetime.now().timetuple()))
    minute_back = int(time.mktime((datetime.now() - timedelta(minutes=1)).timetuple()))
    if not s3.Bucket('bitfinex') in s3.buckets.all():
        s3.create_bucket(Bucket='bitfinex')
    data = get_json_api(services['bitfinex'] + f"start={minute_back}&end={now}")
    obj = s3.Object('bitfinex', f'bitfinex-{datetime.now()}.json')
    obj.put(Body=data)


def push_bitmex_json():
    """pushes bitmex json raw data"""
    now = datetime.utcnow()
    minute_back = datetime.utcnow() - timedelta(minutes=1)
    now_formatted = datetime.strftime(now, '%Y-%m-%d%%20%H%%3A%M')
    minute_back_formatted = datetime.strftime(minute_back, '%Y-%m-%d%%20%H%%3A%M')
    if not s3.Bucket('bitmex') in s3.buckets.all():
        s3.create_bucket(Bucket='bitmex')
    data = get_json_api(services['bitmex']+f'startTime={minute_back_formatted}&endTime={now_formatted}')
    obj = s3.Object('bitmex', f'bitmex-{datetime.now()}.json')
    obj.put(Body=data)


def push_poloniex_json():
    """pushes poloniex json raw data """
    now = int(time.mktime(datetime.now().timetuple()))
    minute_back = int(time.mktime((datetime.now() - timedelta(minutes=1)).timetuple()))
    if not s3.Bucket('poloniex') in s3.buckets.all():
        s3.create_bucket(Bucket='poloniex')
    data = get_json_api(services['poloniex'] + f"start={minute_back}&end={now}")
    obj = s3.Object('poloniex', f'poloniex-{datetime.now()}.json')
    obj.put(Body=data)
