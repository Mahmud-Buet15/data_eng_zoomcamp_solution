import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import datetime
from ingest_data import insert_taxi_trip_data_in_db

current_time = datetime.datetime.now()
formatted_time = current_time.strftime('%Y_%m_%d_%H_%M')

 
dataset_file = "green_tripdata_2019-09.csv"
dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/{dataset_file}.gz"     #f"https://s3.amazonaws.com/nyc-tlc/trip+data/{dataset_file}"
path_to_local_home = os.environ.get("AIRFLOW_HOME")  #if the value for AIRFLOW_HOME not available, /opt/airflow/ will be used as default value

PG_HOST=os.environ.get("PG_HOST_ENV")
PG_USER=os.environ.get("PG_USER_ENV")
PG_PASSWORD=os.environ.get("PG_PASSWORD_ENV")
PG_DB=os.environ.get("PG_DATABASE_ENV")
PG_PORT=os.environ.get("PG_PORT_ENV")


# PG_HOST=os.getenv("PG_HOST")
# PG_USER=os.getenv("PG_USER")
# PG_PASSWORD=os.getenv("PG_PASSWORD")
# PG_DB=os.getenv("PG_DB")


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_local_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de','local'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"wget {dataset_url} && mv {dataset_file}.gz {path_to_local_home}/"   #downloading and moving to home directory
    )
    
    uncompress_dataset_task = BashOperator(
        task_id="uncompress_dataset_task",
        bash_command=f"gunzip -f {path_to_local_home}/{dataset_file}.gz"    # -f overwrites the file
    )

    ingest_data_task= PythonOperator(
        task_id="ingest_data_task",
        python_callable=insert_taxi_trip_data_in_db,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            db=PG_DB,
            port=PG_PORT,
            file_name=dataset_file,
            table_name=f'yellow_taxi_{formatted_time}'
        )
    )


    download_dataset_task >> uncompress_dataset_task >> ingest_data_task