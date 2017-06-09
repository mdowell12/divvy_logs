import sqlite
import postgres

SQLITE_CONST = "sqlite3"
POSTGRES_CONST = "postgres"

# postgres or sqlite3
DATABASE_BACKEND = POSTGRES_CONST


def insert_to_availabilities(row):
    if DATABASE_BACKEND == SQLITE_CONST:
        func = sqlite.insert_to_availabilities
    elif DATABASE_BACKEND == POSTGRES_CONST:
        func = postgres.insert_to_availabilities
    else:
        raise ValueError("Invalid database backend "
                         "selected: {}".format(DATABASE_BACKEND))

    return func(row)


def insert_to_station_blobs(row):
    if DATABASE_BACKEND == SQLITE_CONST:
        func = sqlite.insert_to_station_blobs
    elif DATABASE_BACKEND == POSTGRES_CONST:
        func = postgres.insert_to_station_blobs
    else:
        raise ValueError("Invalid database backend "
                         "selected: {}".format(DATABASE_BACKEND))

    return func(row)
