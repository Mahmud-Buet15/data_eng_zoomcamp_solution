
# GCP-ready Airflow Dockerfile
# First-time build can take upto 10 mins.

FROM apache/airflow:2.2.3

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update -qq && apt-get install vim wget unzip -qqq
# git gcc g++ -qqq

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt                     
RUN pip install --no-cache-dir pandas sqlalchemy psycopg2-binary

 # --no-cache-dir : pip will not store downloaded packages in the cache directory (~/.cache/pip/ by default), and it will not use cached package information during installation. This reduces the size of image.

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID