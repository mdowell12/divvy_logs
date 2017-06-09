import json
import datetime

from divvy_logs import divvy
from divvy_logs import database
from divvy_logs import utils


LOG_DT_FMT = "%Y-%m-%d %H:%M:%S"


def format_for_availabilities(data, queried_at):
    to_return = []

    for row in data:
        new_row = {}
        new_row['queried_at'] = queried_at
        new_row['station_name'] = row['stationName']
        new_row['available_docks'] = int(row['availableDocks'])
        new_row['available_bikes'] = int(row['availableBikes'])
        new_row['total_docks'] = int(row['totalDocks'])

        to_return.append(new_row)

    return to_return


def format_for_station_blobs(data, queried_at):
    to_return = []

    for row in data:
        new_row = {}
        new_row['queried_at'] = queried_at
        new_row['data'] = json.dumps(row)

        to_return.append(new_row)

    return to_return


def log(s):
    now = datetime.datetime.now().strftime(LOG_DT_FMT)
    print "{} {}".format(now, s)


def main():
    queried_at = utils.current_time_in_seconds()
    data = divvy.return_selected_data()

    log("Inserting availability data.")
    formatted_availability_data = format_for_availabilities(data, queried_at)
    for row in formatted_availability_data:
        database.insert_to_availabilities(row)

    log("Inserting blob data.")
    formatted_blobs = format_for_station_blobs(data, queried_at)
    for row in formatted_blobs:
        database.insert_to_station_blobs(row)

    log("Finished inserting data.")


if __name__ == "__main__":
    main()
