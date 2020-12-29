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
