FROM python:3.9.1

RUN pip install pandas

# Setting the working directory of a container
WORKDIR /app                    

# Copying file from host machine to a container
COPY pipeline.py  pipeline.py  

# ENTRYPOINT ["bash"]   # entrupoint: What gets executed after a container starts. Here, bash terminal will open after starting the container

ENTRYPOINT ["python", "pipeline.py"]   # Here, python terminal will open after starting the container and pipeline.py file will be executed