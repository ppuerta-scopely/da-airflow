# da-airflow
Data Academy - Airflow Module

## Repository Structure

- **`dags/`**: Place your DAGs here. Example: `hello_world_dag.py`.
- **`plugins/`**: Custom plugins (operators, hooks, sensors).
- **`include/`**: Auxiliary files used by DAGs (SQL, templates).
- **`logs/`**: Airflow task logs (git ignored).
- **`.airflow/`**: Local Airflow home when running in this repo (git ignored).
- **`requirements.txt`**: Python dependencies.
 - **`.gitignore`**: Common ignores for Python/Airflow projects.

## Prerequisites

- Python 3.10–3.12 installed and available as `python3`.
- Recommended: a virtual environment (e.g., `python3 -m venv .venv && source .venv/bin/activate`).

## Install Dependencies

Airflow recommends installing with constraints matching your Python version.

```bash
python3 -m venv .venv
source .venv/bin/activate

# Find your Python version (e.g., 3.11)
PY_VER=$(python -c 'import sys;print(f"{sys.version_info.major}.{sys.version_info.minor}")')

pip install --upgrade pip
pip install "apache-airflow==2.10.5" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-${PY_VER}.txt"
```
Alternatively, `pip install -r requirements.txt` (constraints still recommended).

## Run Airflow (Quick Start)
Run everything in one command using Airflow Standalone (for local dev):

```bash
# from the repo root
export AIRFLOW_HOME="$(pwd)/.airflow"
airflow standalone
```

This will:

- Initialize the metadata DB.
- Start the webserver and scheduler.
- Create an admin user and print credentials to the console.

Open the UI: http://localhost:8080 and log in with the printed credentials.

## Run with Docker

Build the image (uses `Dockerfile` based on the official Airflow image):

```bash
docker build -t da-airflow:2.10.5 .
```

Run the container for local dev (single-container):

```bash
docker run --rm -it \
  -p 8080:8080 \
  da-airflow:2.10.5
```

## Verify the Example DAG

- In the UI, find the DAG `hello_world` and toggle it On.
- Trigger it manually or wait for the schedule.
- Check task logs to see: `Hello, Airflow!` with the execution date.

## Notes

- If you prefer manual control instead of `airflow standalone`:
  - `export AIRFLOW_HOME="$(pwd)/.airflow"`
  - `airflow db init`
  - In one terminal: `airflow webserver`
  - In another: `airflow scheduler`
  - Create a user if needed: `airflow users create --role Admin --username admin --email admin@example.com --firstname Admin --lastname User --password admin`
- To keep the UI clean, examples are disabled in code; if you still see many example DAGs, set `AIRFLOW__CORE__LOAD_EXAMPLES=False` in your env.
