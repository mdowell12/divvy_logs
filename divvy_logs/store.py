import os

import sqlite3


CUR_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_SQLITE_DB_FILE = os.path.join(CUR_DIR, "../divvy_stats.db")


INSERT_STATS_QUERY = """
    INSERT INTO availabilities VALUES ()

"""

CREATE_AVAILABILITY_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS availabilities (
        id integer,
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
        id integer,
        inserted_at integer,
        queried_at integer,
        data blob
    )
"""


def setup_with_idempotency(db_file=DEFAULT_SQLITE_DB_FILE):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    try:
        cur.execute(CREATE_AVAILABILITY_TABLE_QUERY)
        cur.execute(CREATE_BLOB_TABLE_QUERY)
    except Exception, e:
        print "Error while creating tables: {}".format(e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    setup_with_idempotency()
