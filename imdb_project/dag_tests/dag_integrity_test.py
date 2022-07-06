import pytest
from datetime import datetime
from airflow.models import DagBag


def test_no_import_errors():
    dag_bag = DagBag()
    assert len(dag_bag.import_errors) == 0, "No Import Failures"


def test_retries_zero():
    dag_bag = DagBag()
    for dag in dag_bag.dags:
        retries = dag_bag.dags[dag].default_args.get('retries', [])
        error_msg = f'Retries not set to 0 for DAG {dag}'
        assert retries == 0, error_msg


def test_date_in_past():
    dag_bag = DagBag()
    for dag in dag_bag.dags:
        start_date = dag_bag.dags[dag].default_args.get('start_date', [])
        error_msg = f'start date set not correct for dag {dag}'
        assert start_date < datetime.now(), error_msg


def test_email_correct():
    dag_bag = DagBag()
    for dag in dag_bag.dags:
        email = dag_bag.dags[dag].default_args.get('email', [])
        error_msg = f'Wrong email set for dag {dag}'
        assert email == ['myemail@mail.com'], error_msg
