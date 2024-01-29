#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine
from credentials import get_credentials


def create_db_connection():
    user, password, host, port, db=get_credentials()    
    db_engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print("Database Connection Successful")

    return db_engine


def download_data(url_srting,file_name_string):
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file


    # if url.endswith('.csv.gz'):
    #     csv_name = 'output.csv.gz'
    # else:
    #     csv_name = 'output.csv'

    # os.system(f"wget {url} -O {csv_name}")

    if os.path.isfile(file_name_string): #check if the file already exists in the directory
        print("File already available")
    else: 
        print("Starting download")
        os.system(f"wget {url_srting}")


def insert_zone_data_in_db(url_string, file_name,table_name,db_engine):

    #downloading data 
    download_data(url_string,file_name)                             

    csv_name = file_name
    df = pd.read_csv(csv_name)
    print(df)
    print(df.columns)

    df.to_sql(name=table_name, con=db_engine, if_exists='replace')              #Creating table
    
    print("Finished ingesting zone data into the postgres database") 

def insert_taxi_trip_data_in_db(url_string, file_name,table_name,db_engine):

    #downloading data 
    download_data(url_string,file_name)                             

    #Need to uncompress the file if it's compressed
    csv_name = file_name.replace(".gz","")
    if not os.path.isfile(csv_name):   #checking if the file is available
        os.system(f"gunzip {file_name}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)
    # print(df)
    print(df.columns)
    print(df.head(n=0))
    

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=db_engine, if_exists='replace')   #creating the table
    df.to_sql(name=table_name, con=db_engine, if_exists='append')              #appending the first chunk in the table

    while True: #appending rest of the chunk in the table

        try:
            t_start = time()
            
            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=table_name, con=db_engine, if_exists='append')  

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting taxi trip data into the postgres database")
            break


if __name__ == '__main__':
    db_engine=create_db_connection()
    
    #working with zone data
    url="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
    csv_file_name="taxi+_zone_lookup.csv"
    table_name="ny_zone_data"
    insert_zone_data_in_db(url,csv_file_name,table_name,db_engine)        #inserting zone data to database

    #working with taxi trip data
    url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
    compressed_file_name="green_tripdata_2019-09.csv.gz"
    table_name="ny_green_taxi_tripdata"                    
    # insert_taxi_trip_data_in_db(url,compressed_file_name,table_name,db_engine)   #inserting taxi trip data to database