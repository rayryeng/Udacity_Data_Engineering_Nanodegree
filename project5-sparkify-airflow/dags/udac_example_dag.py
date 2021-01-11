from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

### EDIT - Placed additional default args due to requirements
### of the assignment
default_args = {
    'owner': 'udacity',
    'start_date': datetime(2020, 12, 31),  # HAPPY NEW YEAR!
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False,
    'schedule_interval': '@hourly'
}


dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

### EDIT - Add new input parameters based on specs
stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table='staging_events',
    s3_bucket='udacity-dend',
    s3_key='log_data',
    copy_json_option='s3://udacity-dend/log_json_path.json',
    dag=dag
)

### EDIT - Add new input parameters based on specs
stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table='staging_songs',
    s3_bucket='udacity-dend',
    s3_key='song_data',
    copy_json_option='auto',
    dag=dag
)

### EDIT - Add new input parameters based on specs
load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    redshift_conn_id='redshift',
    table='songplays',
    select_sql=SqlQueries.songplay_table_insert,
    dag=dag
)

### EDIT - Add new input parameters based on specs
load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    redshift_conn_id='redshift',
    table='users',
    select_sql=SqlQueries.user_table_insert,
    append_data=True,
    dag=dag
)

### EDIT - Add new input parameters based on specs
load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    redshift_conn_id='redshift',
    table='songs',
    select_sql=SqlQueries.song_table_insert,
    append_data=True,
    dag=dag
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    redshift_conn_id='redshift',
    table='artists',
    select_sql=SqlQueries.artist_table_insert,
    append_data=True,
    dag=dag
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    redshift_conn_id='redshift',
    table='time',
    select_sql=SqlQueries.time_table_insert,
    append_data=True,
    dag=dag
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    redshift_conn_id='redshift',
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

### EDIT - Build DAG
## Step #1 - Put raw data into staging tables on Redshift
start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift

# Step #2 - Get events and songs data and create songplays table
stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

# Step #3 - From songplays table, create the dimension tables
load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_time_dimension_table

# Step #4 - Run quality checks for the dimension tables
load_user_dimension_table >> run_quality_checks
load_song_dimension_table >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks

# Step #5 - Terminate
run_quality_checks >> end_operator