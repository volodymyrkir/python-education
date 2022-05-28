import boto3
import pandas as pd
from botocore.client import Config
from sqlalchemy import create_engine


def connect_to_s3():
    """Connect to S3(minio) storage"""
    return boto3.client('s3',
                        endpoint_url='http://localhost:9000',
                        aws_access_key_id='root_user',
                        aws_secret_access_key='root_password',
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1')


def connect_to_postgres():
    """Connects to postgres db"""
    engine = create_engine('postgresql://postgres:myPassword@localhost:5432/postgres').connect()
    return engine


def get_s3_keys(connection, bucket_name):
    """Get a list of keys in an S3(minio) bucket."""
    keys = []
    resp = connection.list_objects_v2(Bucket=bucket_name)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys


def translate_columns(unprepared_data):
    """Renames italian columns to american"""
    unprepared_data.rename(
        columns={
            'data': 'date',
            'stato': 'state',
            'codice_regione': 'code_region',
            'denominazione_regione': 'denomination_region',
            'codice_provincia': 'code_province',
            'denominazione_provincia': 'denomination_province',
            'sigla_provincia': 'initials_province',
            'totale_casi': 'total_cases',
            'codice_nuts_1': 'code_nuts_1',
            'codice_nuts_2': 'code_nuts_2',
            'codice_nuts_3': 'code_nuts_3'
        },
        inplace=True
    )


def get_data_concatenated(s3_connection, bucket_name):
    """returns concatenated into 1 csv(table) files from bucket"""
    return pd.concat([pd.read_csv(s3_connection.get_object(Bucket=bucket_name, Key=k).get("Body"))
                      for k in get_s3_keys(s3_connection, bucket_name)], ignore_index=True)


def change_date_format(unprepared_frame):
    """Changes date format"""
    unprepared_frame['date'] = pd.to_datetime(unprepared_frame['date'], format='%Y-%m-%d %H:%M:%S')


def main():
    s3_client = connect_to_s3()
    bucket = 'covid_ita'
    data = get_data_concatenated(s3_client,bucket)
    translate_columns(data)
    change_date_format(data)
    data.to_sql('covid_ita', con=connect_to_postgres(), if_exists='replace', index=False)


if __name__ == "__main__":
    main()
