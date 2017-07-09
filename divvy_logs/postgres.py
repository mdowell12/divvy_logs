import os
import psycopg2 as pg

from utils import current_time_in_seconds
import secret

HOST = "raspberrypidb.c6u7apfikqnb.us-west-2.rds.amazonaws.com"
SCHEMA = "public"
DATABASE = "divvy_logs"
USER = secret.PG_USER
PASSWORD = secret.PG_PASSWORD


CREATE_AVAILABILITY_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS availabilities (
        id bigserial primary key,
        inserted_at integer,
        queried_at integer,
        station_name text,
        available_docks integer,
        available_bikes integer,
        total_docks integer
    );
"""

CREATE_BLOB_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS station_blobs (
        id bigserial primary key,
        inserted_at integer,
        queried_at integer,
        data jsonb
    )
"""

INSERT_TO_AVAILABILITY_QUERY = """
    INSERT INTO availabilities (
        inserted_at,
        queried_at,
        station_name,
        available_docks,
        available_bikes,
        total_docks
    ) VALUES (%s,%s,%s,%s,%s,%s);
"""

INSERT_TO_BLOBS_QUERY = """
    INSERT INTO station_blobs (
        inserted_at,
        queried_at,
        data
    ) VALUES (%s,%s,%s);
"""

READ_AVAILABILITIES_QUERY = """
    SELECT inserted_at,
           queried_at,
           station_name,
           available_docks,
           available_bikes,
           total_docks
    FROM availabilities;
"""


def insert_to_availabilities(row):
    conn = _get_connection()
    cur = conn.cursor()

    try:
        cur.execute(INSERT_TO_AVAILABILITY_QUERY, (
                current_time_in_seconds(),
                row["queried_at"],
                row["station_name"],
                row["available_docks"],
                row["available_bikes"],
                row["total_docks"],
        ))
        conn.commit()
    except Exception, e:
        print "Error inserting to database: {}".format(e)
        raise e
    finally:
        cur.close()
        conn.close()


def insert_to_station_blobs(row):
    conn = _get_connection()
    cur = conn.cursor()

    try:
        cur.execute(INSERT_TO_BLOBS_QUERY, (
                current_time_in_seconds(),
                row["queried_at"],
                row["data"],
        ))
        conn.commit()
    except Exception, e:
        print "Error inserting to database: {}".format(e)
        raise e
    finally:
        cur.close()
        conn.close()


def setup_with_idempotency():
    conn = _get_connection()
    cur = conn.cursor()

    try:
        cur.execute(CREATE_AVAILABILITY_TABLE_QUERY)
        cur.execute(CREATE_BLOB_TABLE_QUERY)
        conn.commit()
    except Exception, e:
        print "Error while creating tables: {}".format(e)
    finally:
        cur.close()
        conn.close()


def read_availabilities_data(start=None, finish=None):
    """
    Read data from availabilities table for range 'start' to 'finish'.
    Defaults to reading whole table.

    :param start: datetime obj
    :param finish: datetime obj
    :return: dict
    """
    if start is not None or finish is not None:
        raise NotImplementedError("Range filtering not yet supported.")

    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(READ_AVAILABILITIES_QUERY)
            data = cur.fetchall()

    return data


def _get_connection():
    return pg.connect(dbname=DATABASE, host=HOST, user=USER, password=PASSWORD)


if __name__ == "__main__":
    setup_with_idempotency()
