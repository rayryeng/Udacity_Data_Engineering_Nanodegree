import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

# Note to self - A staging table is used so that we can
# readily get the raw data into the pipeline in some usable
# form - this is an intermediate form to allow us to finally
# get the data into the actual schema that we are designing

# JSON format of a single event example
# {"artist":"Survivor",
# "auth":"Logged In",
# "firstName":"Jayden",
# "gender":"M",
# "itemInSession":0,
# "lastName":"Fox",
# "length":245.36771,
# "level":"free",
# "location":"New Orleans-Metairie, LA",
# "method":"PUT",
# "page":"NextSong",
# "registration":1541033612796.0,
# "sessionId":100,
# "song":"Eye Of The Tiger",
# "status":200,
# "ts":1541110994796,
# "userAgent":"\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
# "userId":"101"}
staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist varchar,
    auth varchar,
    firstName varchar,
    gender char(1),
    itemInSession int,
    lastName varchar,
    length float,
    level varchar,
    location varchar,
    method varchar,
    page varchar,
    registration float,
    sessionId int,
    song varchar,
    status int,
    ts bigint,
    userAgent varchar,
    userId int
);
""")

# JSON format of a single song example
# {"num_songs": 1,
#  "artist_id": "ARJIE2Y1187B994AB7",
#  "artist_latitude": null,
#  "artist_longitude": null,
#  "artist_location": "",
#  "artist_name": "Line Renaud",
#  "song_id": "SOUPIRU12A6D4FA1E1",
#  "title": "Der Kleine Dompfaff",
#  "duration": 152.92036,
#  "year": 0}
staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs int,
    artist_id varchar,
    artist_latitude float,
    artist_longitude float,
    artist_location varchar,
    artist_name varchar,
    song_id varchar,
    title varchar,
    duration float,
    year int
);
""")

## Note - SERIAL == IDENTITY(0,1) in Redshift
# Also must prefix with int type
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id int IDENTITY(0,1) PRIMARY KEY sortkey, 
    start_time timestamp NOT NULL, 
    user_id int NOT NULL, 
    level varchar, 
    song_id varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    session_id int NOT NULL, 
    location varchar, 
    user_agent varchar
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY distkey, 
    first_name varchar, 
    last_name varchar, 
    gender varchar, 
    level varchar);
""")


song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY, 
    title varchar, 
    artist_id varchar distkey, 
    year int, 
    duration float
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY distkey, 
    name varchar, 
    location varchar, 
    latitude float, 
    longitude float
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time timestamp PRIMARY KEY sortkey distkey, 
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday int
);
""")

# STAGING TABLES
staging_events_copy = ("""
    COPY staging_events
    FROM {}
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    TIMEFORMAT AS 'epochmillisecs'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    FORMAT AS JSON {};
""").format(config.get("S3", "LOG_DATA"), config.get("IAM_ROLE", "ARN"), config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = ("""
    COPY staging_songs
    FROM {}
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    FORMAT AS JSON 'auto' 
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
""").format(config.get("S3", "SONG_DATA"), config.get("IAM_ROLE", "ARN"))

# FINAL TABLES

# INSERT RECORDS
songplay_table_insert = ("""
INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT DISTINCT TIMESTAMP 'epoch' + se.ts/1000 * interval '1 second' AS start_time,
                se.userId AS user_id,
                se.level AS level,
                ss.song_id AS song_id,
                ss.artist_id AS artist_id,
                se.sessionId AS session_id,
                se.location AS location,
                se.userAgent AS user_agent
FROM staging_events se
JOIN staging_songs ss
ON se.song = ss.title AND se.artist = ss.artist_name AND se.length = ss.duration
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
SELECT DISTINCT userId AS user_id,
                firstName AS first_name,
                lastName AS last_name,
                gender AS gender,
                level AS level
FROM staging_events
where userId IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
SELECT DISTINCT song_id AS song_id,
                title AS title,
                artist_id AS artist_id,
                year AS year,
                duration AS duration
FROM staging_songs
WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longitude)
SELECT DISTINCT artist_id AS artist_id,
                artist_name AS name,
                artist_location AS location,
                artist_latitude AS latitude,
                artist_longitude AS longitude
FROM staging_songs
where artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT start_time,
                EXTRACT(hour from start_time),
                EXTRACT(day from start_time),
                EXTRACT(week from start_time),
                EXTRACT(month from start_time),
                EXTRACT(year from start_time),
                EXTRACT(weekday from start_time)
FROM songplays
WHERE start_time IS NOT NULL;
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create,
                        songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop,
                      songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert,
                        song_table_insert, artist_table_insert, time_table_insert]
