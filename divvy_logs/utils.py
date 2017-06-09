import time
import datetime


def current_time_in_seconds():
    return int(time.time())


def current_time_from_epoch(since):
    return datetime.datetime.fromtimestamp(since)
