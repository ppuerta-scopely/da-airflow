from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def _say_hello(execution_date: str, **context):
    print(f"Hello, Airflow! Execution date: {execution_date}")


default_args = {
    "owner": "data-eng",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="hello_world",
    description="A minimal example DAG that prints Hello, Airflow",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["example", "getting-started"],
) as dag:
    say_hello = PythonOperator(
        task_id="say_hello",
        python_callable=_say_hello,
        op_kwargs={"execution_date": "{{ ds }}"},
    )

    # Define task dependencies (single task in this simple DAG)
    say_hello
