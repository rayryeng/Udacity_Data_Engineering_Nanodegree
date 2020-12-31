# Introduction

A startup called Sparkify has grown their user base and song database and want
to move their processes and data onto the cloud. This data currently resides in
an Amazon S3 bucket in a directory of JSON logs that recorded user activity on
their app, as well as a directory with JSON metadata for these songs. The task
is to build an ETL pipeline that extracts the raw data and loads
the data back into S3. This will be a star schema with fact and dimension
tables. The technology we will use for this process is Apache Spark but using
an AWS backend to help do most of the processing for us. Once the data has been
loaded into our star schema, the data can continue to evolve so that Sparkify
can find further insights while removing the burden of on-prem deployment of the
database.

# Project Description

The purpose of this project is to use a data lake and AWS to build an ETL
Pipeline to migrate an existing on-prem database over to the cloud.
The data is already loaded into S3 so that we can properly use the raw data
to extract what we need and allow Spark to do the heavy lifting in bringing the
data over to our fact and dimension tables to finally get transferred over to
the final data model we have in place. This will allow us to finally perform
the required analytics we intend to perform long-term.

# Schema for Song Play Analysis

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

![Proposed Schema](erd.png)

# Project Design

The database design is optimized due to the minimum number of tables needed to
not only represent the data, but to take advantage of as few table joins as
possible to gather the information we need to perform our analysis. The ETL
process is designed to allow reading in the JSON files provided by Sparkify to
be placed in staging tables on Redshift, then finally transitioning the data
over to our final data model.

# Steps

## 1. Create EMR Cluster and Other Preliminaries

We must first create an Amazon EMR Cluster with PySpark. Once this has been
created, you will need to copy the `dl.cfg` and `etl.py` files into the
`/home/hadoop` directory on the master node of cluster through `scp`:
`scp -i path_to_pem_key hadoop@ec2-x-xx-xxx-xxx.compute-1.amazonaws.com`.
Change `path_to_pem_key` to be where your access PEM key for AWS is and
`hadoop@ec2-x-xx-xxx-xxx.compute-1.amazonaws.com` to be the correct DNS of your
EMR cluster.

## 2. Run Main Processing Script

Once we SSH in, please be sure to edit the `output_data` path in the `etl.py`
script to a S3 bucket that exists. The path currently is set to one that did
exist for the completion of this project but it no longer does to avoid
incurring charges. Please use `nano etl.py` to edit the `output_data` path in
the file.

After editing, we must run the `etl.py` file in the terminal using the
`spark-submit` command: `/usr/bin/spark-submit --master yarn ./etl.py`. If you
happen to get an error mentioning `configparser` cannot be found, please install
it first by `sudo pip install configparser` prior to running the script. This
script accomplishes the loading of the raw data into Spark dataframes the
transitioning over to the final data model. Please note that at the time that
this project was completed, the full dataset available from Udacity took between
10-20 minutes using a `m5.large` Spark cluster wih 1 master node and 3 slave
nodes. Keep this timeframe in mind should you attempt to execute the ETL
pipeline.

# Summary of Relevant Files

- `etl.py`: The final processing script to process read in the data from S3 and
  ultimately does the transfer to the final data model on Spark.
- `README.md`: This file.
- `erd.png`: Entity Relationship Diagram of the proposed schema
- `dl.cfg`: The configuration file so that we can connect to our Amazon
  Spark cluster. Please note that the access and secret key have been removed
  due to privacy reasons so you will need to put these in yourself if you want
  to run the script.
