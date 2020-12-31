import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, dayofweek
from pyspark.sql.types import TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID'] = config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Function to create a new Spark session which we will use for populating
    tables and writing Parquet files.

    Returns:
        A new Spark session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Function to create a consolidated Spark dataframe from the song data,
    then create the required songs and artists tables to be written to
    S3 as Parquet files.

    Inputs:
        spark: The current Spark session
        input_data: The S3 path to the input log and song files
        output_data: The output S3 path to write our Parquet files
    """
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'

    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select('song_id', 'title', 'artist_id',
                            'year', 'duration') \
        .dropDuplicates(subset=['song_id'])

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy(
        'year', 'artist_id').parquet(output_data + '/songs_table')

    # extract columns to create artists table
    artists_table = df.select('artist_id', 'artist_name', 'artist_location',
                              'artist_latitude', 'artist_longitude') \
        .withColumnRenamed('artist_name', 'name') \
        .withColumnRenamed('artist_location', 'location') \
        .withColumnRenamed('artist_latitude', 'latitude') \
        .withColumnRenamed('artist_longitude', 'longitude') \
        .dropDuplicates(subset=['artist_id'])

    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(
        output_data + '/artists_table')


def process_log_data(spark, input_data, output_data):
    """
    Function to create a consolidated Spark dataframe from the log data,
    then create the required users, time and songplays tables to be written to
    S3 as Parquet files.

    Inputs:
        spark: The current Spark session
        input_data: The S3 path to the input log and song files
        output_data: The output S3 path to write our Parquet files
    """
    # get filepath to log data file
    log_data = input_data + 'log_data/*/*/*.json'

    # read log data file
    df = spark.read.json(log_data)

    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table
    users_table = df.select('userId', 'firstName',
                            'lastName', 'gender', 'level') \
        .dropDuplicates(subset=['userId'])

    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(output_data + '/users_table')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: int(x) // 1000)
    df = df.withColumn('timestamp', get_timestamp('ts'))

    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: datetime.fromtimestamp(x), TimestampType())
    df = df.withColumn('start_time', get_datetime('timestamp'))

    # extract columns to create time table
    time_table = df.select('start_time') \
        .withColumn('hour', hour('start_time')) \
        .withColumn('day', dayofmonth('start_time')) \
        .withColumn('week', weekofyear('start_time')) \
        .withColumn('month', month('start_time')) \
        .withColumn('year', year('start_time')) \
        .withColumn('weekday', dayofweek('start_time')) \
        .dropDuplicates(subset=['start_time'])

    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy(
        'year', 'month').parquet(output_data + '/time_table')

    # read in song data to use for songplays table
    song_df = spark.read.json(input_data + 'song_data/*/*/*/*.json')

    # extract columns from joined song and log datasets to create songplays
    # table - note: We must reintroduce year and month into dataframe in order
    # for us to properly partition
    songplays_table = df.join(song_df, df.artist == song_df.artist_name) \
                        .select('start_time', 'userId', 'song_id', 'artist_id',
                                'level', 'sessionId', 'location', 'userAgent') \
                        .withColumn("year", year("start_time")) \
                        .withColumn("month", month("start_time")) \
                        .dropDuplicates() \
                        .withColumn("songplay_id", monotonically_increasing_id())

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode('overwrite').partitionBy(
        'year', 'month').parquet(output_data + '/songplays_table')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend-rayryeng/"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
