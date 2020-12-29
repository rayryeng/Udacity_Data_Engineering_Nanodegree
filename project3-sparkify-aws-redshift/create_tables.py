import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Function that drops any existing staging and final tables on Amazon Redshift so we can start from scratch

    Args:
        cur: psycopg2 cursor object establishing a connection to our database
        conn - The corresponding psycopg2 connection to the Amazon Redshift cluster we have open

    Returns:
        None
    """

    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Function that initially creates our staging and final tables on Amazon Redshift

    Args:
        cur: psycopg2 cursor object establishing a connection to our database
        conn - The corresponding psycopg2 connection to the Amazon Redshift cluster we have open

    Returns:
        None
    """

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
        *config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
