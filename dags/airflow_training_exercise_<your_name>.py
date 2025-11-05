from __future__ import annotations
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule

import random

# Generate a random number of rows
def transform(**context):
    rows = random.randint(0, 100)
    context["ti"].xcom_push(key="row_count", value=rows)
    print(f"Processed {rows} rows.")

# Validate against a threshold (pulled from DAG params)
def validate(**context):
    threshold = context["dag"].params.get("min_valid_rows", 40)
    rows = context["ti"].xcom_pull(key="row_count", task_ids="transform_data")
    is_valid = (rows or 0) >= threshold
    context["ti"].xcom_push(key="is_valid", value=is_valid)
    print(f"Validated {rows} rows against threshold={threshold} → valid={is_valid}")

# Branch depending on validation result
def choose_branch(**context) -> str:
    is_valid = context["ti"].xcom_pull(key="is_valid", task_ids="validate_data")
    return "load_to_dw" if is_valid else "skip_load"

# Simple QC checks
def qc_nulls(**_):
    print("Null check passed.")

def qc_ranges(**_):
    print("Range check passed.")

def qc_summary(**context):
    rows = context["ti"].xcom_pull(key="row_count", task_ids="transform_data")
    print(f"QC summary for {rows} rows.")

# Notifications
def notify_success(**_):
    print("Pipeline succeeded.")

def notify_skipped(**_):
    print("Load skipped due to validation failure.")


default_args = {"owner": "data-eng", "retries": 1, "retry_delay": timedelta(minutes=2)}

with DAG(
    dag_id="airflow_training_exercise_<your_name>", #PLEASE ADD YOUR NAME HERE AND IN THE FILENAME
    description="Training DAG for Airflow Hands-on Exercise",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["training", "example", "branching", "broken"],
    params={"min_valid_rows": 40},
) as dag:

    # Start
    start = EmptyOperator(task_id="start")

    # Wait a few seconds before starting
    wait_a_bit = BashOperator(task_id="wait_a_bit", bash_command="sleep 10")

    # Extract data
    extract_data = BashOperator(
        task_id="extract_data",
        bash_command="echo 'Extracting data...' && sleep 1 && echo 'Done'",
    )

    # Transform data
    transform_data = PythonOperator(task_id="transform_data", python_callable=transform)

    # Validate data
    validate_data = PythonOperator(task_id="validate_data", python_callable=validate)

    # Decide whether to load or skip
    decide = BranchPythonOperator(task_id="decide_to_load", python_callable=choose_branch)

    # Load to data warehouse
    load_to_dw = BashOperator(
        task_id="load_to_dw",
        bash_command="echo 'Loading to DW...' && sleep 1 && echo 'OK'",
    )

    # Skip load if validation failed
    skip_load = PythonOperator(task_id="skip_load", python_callable=notify_skipped)

    # Data quality checks (group)
    with TaskGroup(group_id="data_quality") as data_quality:
        qc_check_nulls = PythonOperator(task_id="qc_check_nulls", python_callable=qc_nulls)
        qc_check_ranges = PythonOperator(task_id="qc_check_ranges", python_callable=qc_ranges)

    # Join both branches (branch-unfriendly trigger)
    join = EmptyOperator(
        task_id="join",
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    # Notify success (inherits default ALL_SUCCESS)
    notify_ok = PythonOperator(
        task_id="notify_success",
        python_callable=notify_success,
    )

    # Orphan task (never connected)
    cleanup_tmp = BashOperator(
        task_id="cleanup_tmp",
        bash_command="echo 'Cleaning tmp...' && sleep 1 && echo 'OK'",
    )

    start = EmptyOperator(task_id="start")

    end = EmptyOperator(task_id="end")
    
    skip_load >> validate_data

    start >> wait_a_bit >> extract_data >> transform_data >> validate_data >> decide
    decide >> load_to_dw >> data_quality >> join
    decide >> skip_load >> join
    join >> notify_ok >> end

    cleanup_tmp