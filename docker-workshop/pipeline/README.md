# SQL queries used in homework

## Question 4.
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).
Use the pick up time for your calculations.
```sql
select DATE(lpep_pickup_datetime) as trip_date, sum(trip_distance) as daily_distance from public.green_taxi_trips 
where lpep_pickup_datetime >= '2025-11-01 00:00:00' and lpep_pickup_datetime < '2025-12-01 00:00:00' and trip_distance <= 100
group by DATE(lpep_pickup_datetime)
order by daily_distance desc;
```

## Question 5.
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?
```sql
select z_pu."Zone", sum(total_amount) as total from green_taxi_trips t
join taxi_zone z_pu on t."PULocationID" = z_pu."LocationID"
join taxi_zone z_do on t."DOLocationID" = z_do."LocationID"
where date(lpep_pickup_datetime) = '2025-11-18'
group by z_pu."Zone"
order by total desc
limit 10;
```


## Question 6.
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?
Note: it's tip , not trip. We need the name of the zone, not the ID.
```sql
select t.tip_amount, z_do."Zone" from green_taxi_trips t
join taxi_zone z_pu on t."PULocationID" = z_pu."LocationID"
join taxi_zone z_do on t."DOLocationID" = z_do."LocationID"
where z_pu."Zone" = 'East Harlem North' and t.lpep_pickup_datetime >= '2025-11-01 00:00:00' and lpep_pickup_datetime < '2025-12-01 00:00:00'
order by t.tip_amount desc;
```

link to the source homework:
https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/01-docker-terraform/homework.md


# How to run python files and load data into db?
### 1. Setup docker compose
```bash
  docker compose build -t
```
### 2. Download parquet file with green_taxi_trips
```bash
  wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
```
### 3. Run uv with python script
```bash
  uv run green_taxi_trips.py 
```

### 4. Go to the pgAdmin and play with data
