#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def create_db_connection(user, password, host, db, port): 
    print(user, password, host, db, port)
    db_engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print("Database Connection Successful")

    return db_engine


def insert_taxi_trip_data_in_db(user, password, host, db, port, file_name,table_name):     
    print("Trying to authenticate")
    db_engine=create_db_connection(user, password, host, db, port)

    df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
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