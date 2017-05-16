import json
import requests


JSON_API_URL = 'http://feeds.divvybikes.com/stations/stations.json'
DEFAULT_STATION_NAMES = (

    ### WORK ###
    'Ogden Ave & Race Ave',
    'Dearborn St & Adams St',
    'Dearborn St & Monroe St',
    'LaSalle St & Adams St',

    ### HOME ###
    'LaSalle St & Jackson Blvd',
    'Ashland Ave & Grand Ave',
    'Eckhart Park',
    'Ogden Ave & Chicago Ave',
)


def return_selected_data(stations=None, url=None):
    return parse_stations(stations_from_raw_json(fetch()))


def fetch(url=JSON_API_URL):
    res = requests.get(url)

    if not res.status_code == 200:
        print "Bad API request.  Status code: {}".format(res.status_code)

    return res.json()


def stations_from_raw_json(data):
    return data['stationBeanList']


def timestamp_from_raw_json(data):
    return data['executionTime']


def parse_stations(station_list, stations=None):

    if stations is None:
        stations = DEFAULT_STATION_NAMES
    
    selected_stations = filter(lambda x: x['stationName'] in stations, station_list)
    selected_stations_dict = {data['stationName']: data for data in selected_stations}

    for station in stations:
        if station not in selected_stations_dict:
            print "WARNING: Station %s not found in selected stations " % station + \
                  "list: %s" % selected_stations_dict.keys()

    return selected_stations


if __name__ == "__main__":
    data = return_selected_data()
    print data[0]

