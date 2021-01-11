# Udacity Data Engineering Nanodegree Course

In this repo, it contains the projects I worked on for the Data Engineering
Nanodegree course on Udacity. Each project is separated into directories. For
each applicable directory, a README markdown file is accompanied with the
directory to describe the purpose of the project as well as the required steps
to complete the project.

# Project 1 - Data Modelling with PostgreSQL

This project deals with building an ETL pipeline for a fictional startup called
Sparkify. We will need to define fact and dimension tables for a star schema and
write an ETL pipeline that transfers data from JSON files in two local directories
into these tables in Postgres using Python and SQL. The accompanying README
provides a further summary of the project, as well as a description of how to
run the project from end to end.

# Project 2 - Data Modelling with Apache Cassandra

The same fictional startup Sparkify would like to build a database with Apache
Cassandra as well as complete an ETL pipeline in Python. For this project, we
wish to understand what songs users are listening to as there is no easy way to
query these results. The ETL pipeline will be used to load in data from CSV
files in order to provide the queries needed to answer the analysis questions
required by Sparkify. Please note that there is no README associated with this
project and all that is required is to open up the `Project_1B.ipynb` notebook
file and to run the cells from start to finish.

# Project 3 - Data Modelling with Amazon Redshift

The same fictional startup Sparkify would like to build a database end-to-end
with Amazon Redshift. Specifically, this would be in the same spirit as
Project #2, except the ETL pipeline and loading into the final data model
is done completely through Amazon Redshift. First the raw data is copied
and loaded onto staging tables that serve as an intermediary to ensure we
can load in all of the data correctly to allow for the next step to be easier
to perform, which is actually loading the data onto the fact and dimension
tables that were designed for future analyses of the songs and users as per
Project #1. The accompanying README provides a further summary of the project,
as well as a description of how to run the project from end to end.

# Project 4 - Data Lake with Amazon EMR Cluster

The same fictional startup Sparkify would now like to use a data lake and AWS
to build an ETL Pipeline to migrate an existing on-prem database over to the
cloud. The data is already loaded into S3 so that we can properly use the raw
data to extract what we need and allow Spark to do the heavy lifting in
bringing the data over to our fact and dimension tables to finally get
transferred over to the final data model we have in place. This will allow us
to finally perform the required analytics we intend to perform long-term.

# Project 5 - Data Pipelines with Airflow

The same fictional company, Sparkify, has decided that it is time to introduce
more automation and monitoring to their data warehouse ETL pipelines and come to
the conclusion that the best tool to achieve this is Apache Airflow. In
particular, we will create high grade data pipelines that are dynamic and
built from reusable tasks, can be monitored, and allow easy backfills. The
source data resides in S3 and needs to be processed in Sparkify's data warehouse
in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.
