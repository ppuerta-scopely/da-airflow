ARG AIRFLOW_VERSION=2.10.5
FROM apache/airflow:latest

USER airflow
COPY requirements.txt /requirements.txt
RUN set -eux; \
    PY_VER=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")'); \
    pip install --no-cache-dir -r /requirements.txt 

USER airflow
COPY --chown=airflow:root plugins/ /opt/airflow/plugins/
COPY --chown=airflow:root include/ /opt/airflow/include/

ENV AIRFLOW__CORE__LOAD_EXAMPLES=True
EXPOSE 8080

# Simple single-container dev run
CMD ["airflow", "standalone"]

