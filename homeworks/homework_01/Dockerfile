FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2-binary

# Setting the working directory of a container
WORKDIR /app                    

# Copying file from host machine to a container
COPY ingest_data.py  ingest_data.py  
COPY credentials.py  credentials.py 

# entrypoint: What gets executed after a container starts. Here, bash terminal will open after starting the container
# ENTRYPOINT ["bash"]   

# Here, python terminal will open after starting the container and pipeline.py file will be executed
ENTRYPOINT ["python", "ingest_data.py"]   