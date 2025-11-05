# dags/demo_top10_native_operators_2_10.py
from __future__ import annotations

import pendulum
from datetime import timedelta
from random import random

from airflow import DAG

# Core operators (Airflow 2.10)
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


# ---- Python callables -------------------------------------------------------
def compute_stats(**context):
    print("Computing stats...")
    return 42


def pick_branch(**context) -> str:
    return "branch_true" if random() > 0.5 else "branch_false"


def gate_condition(**context) -> bool:
    return True


# ---- DAG --------------------------------------------------------------------
with DAG(
    dag_id="airflow_training_20251007_operators",
    start_date=pendulum.datetime(2025, 1, 1, tz="Europe/Madrid"),
    schedule="@daily",             
    catchup=False,
    description="5 different Airflow Operators",
    default_args={"retries": 1},
    tags=["demo", "operators"],
) as dag:

    # 5) EmptyOperator — start
    start = EmptyOperator(task_id="start")

    # 1) BashOperator
    bash = BashOperator(task_id="bash_hello", bash_command='echo "Hello from BashOperator!"')

    # 2) PythonOperator
    py = PythonOperator(task_id="python_compute", python_callable=compute_stats)

    # 3) BranchPythonOperator
    branch = BranchPythonOperator(task_id="branch_decision", python_callable=pick_branch)
    branch_true = EmptyOperator(task_id="branch_true")
    branch_false = EmptyOperator(task_id="branch_false")

    join = EmptyOperator(
        task_id="join_after_branch",
        trigger_rule='all_done',
    )

    bash2 = BashOperator(
         task_id="get_joke",
         bash_command='curl -s https://official-joke-api.appspot.com/random_joke'
    )

    # 7) TriggerDagRunOperator
    trigger_other = TriggerDagRunOperator(
        task_id="trigger_other_dag",
        trigger_dag_id="target_downstream_dag_id",  # <-- update to an existing DAG id
        conf={"source": "demo_top10_native_operators_2_10"},
        reset_dag_run=True,
        wait_for_completion=False,
    )

    end = EmptyOperator(task_id="end")

    # ---- Dependencies --------------------------------------------------------
    start >> [bash, bash2] >> py >> branch
    branch >> [branch_true, branch_false] >> join
    join >> trigger_other >> end
