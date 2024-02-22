# Essential information to understand Airflow

The base Airflow Docker image won't work with GCP, so we need to customize it to suit our needs. A few things of note:
- We use the base Apache Airflow image as the base.
- We install the **GCP SDK CLI tool** so that Airflow can communicate with our GCP project.
- We also need to provide a **requirements.txt** file to install Python dependencies. The dependencies are:
    - `apache-airflow-providers-google` so that Airflow can use the GCP SDK.
    - `pyarrow` , a library to work with parquet files.

## Setting up airflow locally

### Pre-requisites
- This tutorial assumes that the service account credentials JSON file is named **google_credentials.json** and stored in `$HOME/.google/credentials/`. Copy and rename your credentials file to the required path.
- `docker-compose` should be at least version v2.x+ and Docker Engine should have **at least 5GB of RAM** available, ideally 8GB. On Docker Desktop this can be changed in `Preferences > Resources`.

### Managing Google cloud credentials
- `cd ~ && mkdir -p ~/.google/credentials/`
- `mv <path_to_your_service-account-authkeys>.json ~/.google/credentials/google_credentials.json`

### Adding User variable
- `echo -e "AIRFLOW_UID=$(id -u)" > .env`

### Run docker commands
- Build the images
    - `docker compose build` or `docker-compose build`

- Create the containers
    - `docker compose up` or `docker-compose up`
    - `docker compose up -d` or `docker-compose up -d`    [detached mode]

- Remove the containers
    - `docker compose down` or `docker-compose down`