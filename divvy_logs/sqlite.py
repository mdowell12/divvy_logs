import os
import sqlite3

from utils import current_time_in_seconds


CUR_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SQLITE_DB_FILE = os.path.join(CUR_DIR, "../divvy_stats.db")


CREATE_AVAILABILITY_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS availabilities (
        id integer primary key,
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
        id integer primary key,
        inserted_at integer,
        queried_at integer,
        data blob
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
    ) VALUES (?,?,?,?,?,?);
"""

INSERT_TO_BLOBS_QUERY = """
    INSERT INTO station_blobs (
        inserted_at,
        queried_at,
        data
    ) VALUES (?,?,?);
"""


def insert_to_availabilities(row, db_file=DEFAULT_SQLITE_DB_FILE):
    conn = sqlite3.connect(db_file)
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


def insert_to_station_blobs(row, db_file=DEFAULT_SQLITE_DB_FILE):
    conn = sqlite3.connect(db_file)
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


def setup_with_idempotency(db_file=DEFAULT_SQLITE_DB_FILE):
    conn = sqlite3.connect(db_file)
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


if __name__ == "__main__":
    setup_with_idempotency()
