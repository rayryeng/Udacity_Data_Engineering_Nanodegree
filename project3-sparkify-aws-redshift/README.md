# Introduction

A startup called Sparkify has grown their user base and song database and want
to move their processes and data onto the cloud. This data currently resides in
an Amazon S3 bucket in a directory of JSON logs that recorded user activity on
their app, as well as a directory with JSON metadata for these songs. The task
is to build an ETL pipeline that extracts the raw data and places them into
staging tables as an intermediary to allow for easy loading onto the actual
schema that was designed for easy analytics and processing after the fact. This
will be a star schema with fact and dimension tables. The technology we will use
for this process is Amazon Redshift. Once the data has been loaded into our star
schema, the data can continue to evolve so that Sparkify can find further
insights while removing the burden of on-prem deployment of the database.

# Project Description

The purpose of this project is to use a data warehouse and AWS to build an ETL
Pipeline to migrate an existing on-prem database over to Redshift. The data is
already loaded into S3 so that we can properly load the raw data into staging
tables which will then get transferred over to the final data model we have in
place. Using Redshift, we will execute SQL Statements to create the fact and
dimension tables from these staging tables to finally perform the required
analytics we intend to perform long-term.

# Schema for Song Play Analysis

## Staging Tables

An example of the raw data coming in for a single event that happened on
Sparkify's app is the following:

```
{"artist":"Survivor",
 "auth":"Logged In",
 "firstName":"Jayden",
 "gender":"M",
 "itemInSession":0,
 "lastName":"Fox",
 "length":245.36771,
 "level":"free",
 "location":"New Orleans-Metairie, LA",
 "method":"PUT",
 "page":"NextSong",
 "registration":1541033612796.0,
 "sessionId":100,
 "song":"Eye Of The Tiger",
 "status":200,
 "ts":1541110994796,
 "userAgent":"\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
 "userId":"101"}
```

Each field in this example JSON was modelled appropriately with the correct
input types and an appropriate SQL copy command was executed to allow us to
populate the staging table with minimal effort.

An example of the raw data for a single song on Sparkify's app is the following:

```
{"num_songs": 1,
 "artist_id": "ARJIE2Y1187B994AB7",
 "artist_latitude": null,
 "artist_longitude": null,
 "artist_location": "",
 "artist_name": "Line Renaud",
 "song_id": "SOUPIRU12A6D4FA1E1",
 "title": "Der Kleine Dompfaff",
 "duration": 152.92036,
 "year": 0}
```

Each field in this example JSON was modelled appropriately with the correct
input types and an appropriate SQL copy command was executed to allow us to
populate the staging table with minimal effort.

## Fact Table

`songplays` records the log data from users that is associated with song plays
i.e. records with page `NextSong`.

- _Columns_: `songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent`

## Dimension Tables

We have the following dimension tables:

- `users`: Are the users in the streaming app.
  - _Columns_: `user_id, first_name, last_name, gender, level`.
- `songs`: Are the songs in the music database.
  - _Columns_: `song_id, title, artist_id, year, duration`
- `artists`: Are the artists in music database.
  - _Columns_: `artist_id, name, location, latitude, longitude`
- `time`: Are the timestamps of logs in songplays decomposed into specific units
  of time.
  - _Columns_: `start_time, hour, day, week, month, year, weekday`

## Entity Relationship Diagram of the Proposed Schema

Please note that this uses the exact same schema as Project #1, but the
staging table receives the timestamp in `bigint`. The fact table will
ultimately convert the timestamp into its appropriate format. In addition,
the gender has been changed to a single `char` as opposed to a `varchar`.

![Proposed Schema](erd.png)

# Project Design

The database design is optimized due to the minimum number of tables needed to
not only represent the data, but to take advantage of as few table joins as
possible to gather the information we need to perform our analysis. The ETL
process is designed to allow reading in the JSON files provided by Sparkify to
be placed in staging tables on Redshift, then finally transitioning the data
over to our final data model.

# Steps

## 1. Run Database Script

We must first initialize our database and tables on Redshift. Running
`python create_tables.py` in the terminal allows this to happen.

## 2. Run Main Processing Script

Once we have completed the above steps, we must run the `etl.py` file in the
terminal: `python etl.py`. This accomplishes the two-fold process of loading the
raw data into staging tables, then transitioning over to the final data model.
This is all done on Amazon Redshift which carries out our ETL pipeline.
Please note that at the time that this project was completed, the full dataset
available from Udacity took between 10-20 minutes using a `d2c.large` Redshift
cluster with 4 cores. Keep this timeframe in mind should you attempt to execute
the ETL pipeline.

## 3. Verify accuracy

Once the processing has been completed, test queries using the Query Editor on
Amazon Redshift were used to verify that the data was successfully loaded in.
For closure, there is a `test.ipynb` test notebook file that allows us to
connect with the database on Amazon Redshift and we will provide sample queries
to show that the data model is properly populated.

# Summary of Relevant Files

- `sql_queries.py`: Contains strings that contain SQL queries for dropping,
  creating and inserting into the staging and final tables on Redshift we need
  for this project.
- `create_tables.py`: Drops any of the tables in the project should they exist
  and recreates them on Redshift. We initially initialize our tables from
  scratch.
- `etl.py`: The final processing script to process read in the data from S3 and
  places them in the staging tables, then ultimately does the transfer to the
  final data model on Redshift.
- `README.md`: This file.
- `erd.png`: Entity Relationship Diagram of the proposed schema
- `test.ipynb`: Test notebook file that connects to the Amazon Redshift database
  once we have run the ETL pipeline and shows example queries to verify proper
  population of the tables.
- `dwh.cfg`: The configuration file so that we can connect to our Amazon
  Redshift cluster. The connection details have been left in the file for
  posterity, but the Redshift cluster has been removed not only for security
  reasons but to avoid incurring unnecessary charges.
