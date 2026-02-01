Queries used in homework

flow name: gcp_taxi_scheduled.yaml

Question 3. How many rows are there for the Yellow Taxi data for all CSV files in the year 2020? 
```sql
SELECT count(*) FROM `kestra-46056.zoomcamp.yellow_tripdata` 
WHERE REGEXP_CONTAINS(filename, r'2020-0[1-9]\.csv')
   OR REGEXP_CONTAINS(filename, r'2020-1[0-2]\.csv');
```
Question 4. How many rows are there for the Green Taxi data for all CSV files in the year 2020
```sql
SELECT count(*) FROM `kestra-46056.zoomcamp.green_tripdata` 
WHERE REGEXP_CONTAINS(filename, r'2020-0[1-9]\.csv')
   OR REGEXP_CONTAINS(filename, r'2020-1[0-2]\.csv');
   ```

Question 5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file? 
```sql
SELECT count(*) FROM `kestra-46056.zoomcamp.yellow_tripdata` 
WHERE REGEXP_CONTAINS(filename, r'2021-03.csv')
```