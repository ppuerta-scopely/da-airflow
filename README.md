# Data Academy - Airflow Hands-on Excercise
Data Academy - Airflow Module

## Repository Structure

- **`dags/`**: Place your DAGs here. Example: `hello_world_dag.py`.
- **`plugins/`**: Custom plugins (operators, hooks, sensors).
- **`include/`**: Auxiliary files used by DAGs (SQL, templates).
- **`logs/`**: Airflow task logs (git ignored).
- **`.airflow/`**: Local Airflow home when running in this repo (git ignored).
- **`requirements.txt`**: Python dependencies.
 - **`.gitignore`**: Common ignores for Python/Airflow projects.

## Run Airflow (Quick Start)

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
