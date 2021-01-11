# Introduction

A music streaming company, Sparkify, has decided that it is time to introduce
more automation and monitoring to their data warehouse ETL pipelines and come
to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high
grade data pipelines that are dynamic and built from reusable tasks, can be
monitored, and allow easy backfills. They have also noted that the data quality
plays a big part when analyses are executed on top the data warehouse and want
to run tests against their datasets after the ETL steps have been executed to
catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data
warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell
about user activity in the application and JSON metadata about the songs the
users listen to.

# Project Overview

This project will introduce you to the core concepts of Apache Airflow. To
complete the project, you will need to create your own custom operators to
perform tasks such as staging the data, filling the data warehouse, and running
checks on the data as the final step.

We have provided you with a project template that takes care of all the imports
and provides four empty operators that need to be implemented into functional
pieces of a data pipeline. The template also contains a set of tasks that need
to be linked to achieve a coherent and sensible data flow within the pipeline.

You'll be provided with a helpers class that contains all the SQL
transformations. Thus, you won't need to write the ETL yourselves, but you'll
need to execute it with your custom operators.

The DAG that we will be setting up is shown below:

![DAG for project](example-dag.png)

# Steps

1. Follow the instructions on Udacity for adding the Airflow connections for
   the AWS and Redshift credentials (you'll need to be enrolled on the data
   engineering nanodegree to see these instructions)

2. Open up the Udacity workspace that houses the necessary files to complete
   this project.

3. Go into the `dags` subdirectory, then open up the `udac_example_dag.py` file
   and replace the contents of the file on the workspace with the corresponding
   file on the workspace.

4. Go into the `operators` subdirectory, then for each of the files in this
   subdirectory, replace the file contents on the workspace with the
   corresponding file on the workspace.

5. Click on the "Access Airflow" button in the workspace.

6. In the Airflow UI that pops up, in the DAGs page, turn on the
   `udac_example_dag` DAG and let it execute.

7. You can check the logs to see if it completed successfully, but it should.
