import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Function that will process the raw song and event data currently on S3
    and loads them into their staging tables.

    Args:
        cur: psycopg2 cursor object establishing a connection to our database
        conn - The corresponding psycopg2 connection to the Amazon Redshift cluster we have open

    Returns:
        None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Function that reads data from our staging tables and place into our final data model
    following the star schema on Redshift.

    Args:
        cur: psycopg2 cursor object establishing a connection to our database
        conn - The corresponding psycopg2 connection to the Amazon Redshift cluster we have open

    Returns:
        None
    """

    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
        *config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
