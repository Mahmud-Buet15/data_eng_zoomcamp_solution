## Question 1. Knowing docker tags
- Command: docker run --help
- Answer: --rm

## Question 2. Understanding docker first run
- Commands: docker run -it --entrypoint=bash python:3.9
- Answer: 0.42.0

## Prepare Postgres
    - Creating postgres database and pgAdmin containers
    - Ingesting data in database

## Question 3. Count records
- Question: How many taxi trips were totally made on September 18th 2019?

- Query 1: Considering the trips which started on September 18th 2019
```
select 
	count(1) as total_trips
from ny_taxi.public.ny_green_taxi_tripdata
where 1=1
and date(lpep_pickup_datetime)='2019-09-18'
```
- Answer: 15767

- Query 2: Considering the trips which started and ended on September 18th 2019
```
select 
	count(1) as total_trips
from ny_taxi.public.ny_green_taxi_tripdata
where 1=1
and date(lpep_pickup_datetime)='2019-09-18'
and date(lpep_dropoff_datetime)='2019-09-18'
;
```
- Answer: 15612


## Question 4. Largest trip for each day
- Question: Which was the pick up day with the largest trip distance. Use the pick up time for your calculations.

- Query :
```
select 
	date(lpep_pickup_datetime) as pick_up_date
from ny_taxi.public.ny_green_taxi_tripdata
order by trip_distance desc 
limit 1
;
```

- Answer: 2019-09-26


## Question 5. Three biggest pick up Boroughs
- Question: Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000? [Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown]

- Query :
```
select 
	tbl2."Borough"
    , sum(total_amount) as total_amount_
from ny_taxi.public.ny_green_taxi_tripdata tbl1 
inner join ny_taxi.public.ny_zone_data tbl2 on tbl1."PULocationID"=tbl2."LocationID"
where 1=1
and date(lpep_pickup_datetime)='2019-09-18'
group by 1
having sum(total_amount)>50000
order by 2 desc
;
```

- Answer: "Brooklyn" "Manhattan" "Queens"


## Question 6. Largest tip
- Question: For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip. We want the name of the zone, not the id.

- Query :
```
select 
	tbl3."Zone"
from ny_taxi.public.ny_green_taxi_tripdata tbl1 
inner join ny_taxi.public.ny_zone_data tbl2 on tbl1."PULocationID"=tbl2."LocationID" and tbl2."Zone"='Astoria'
inner join ny_taxi.public.ny_zone_data tbl3 on tbl1."DOLocationID"=tbl3."LocationID" 
where 1=1
and date(date_trunc('month',lpep_pickup_datetime))='2019-09-01'
order by tip_amount desc
limit 1
;
```

- Answer: "JFK Airport"