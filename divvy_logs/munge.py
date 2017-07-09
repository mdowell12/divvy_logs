import pandas as pd
import datetime


COLUMNS = ('inserted_at', 'queried_at', 'station_name',
           'available_docks', 'available_bikes', 'total_docks')

def prep(data):
    """
    :param data: list of dicts
    :return: DataFrame
    """
    df = pd.DataFrame(data, columns=COLUMNS)
    df = _prep_timestamp_columns(df, ('inserted_at', 'queried_at',))
    df = _add_analytics(df)

    return df


def _prep_timestamp_columns(df, columns):
    for col in columns:
        df[col] = df[col].apply(lambda x: datetime.datetime.fromtimestamp(x))

    return df


def _add_analytics(df):
    df['day_of_week'] = df['queried_at'].dt.weekday_name
    df['queried_at_hour'] = df['queried_at'].dt.hour
    return df


if __name__ == "__main__":
    import database
    data = database.read_availabilities_data()

    df = prep(data)
    import pdb; pdb.set_trace()
