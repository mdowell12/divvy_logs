import dash
import dash_core_components as dcc
import dash_html_components as html

from database import read_availabilities_data
from munge import prep

app = dash.Dash()

data = read_availabilities_data()
df = prep(data)

grouped = df.groupby(['station_name', 'day_of_week']).mean()
station_names = set(grouped.index.get_level_values(0))

docks_graph_data = []
for station in station_names:
    sub_df = grouped.loc[station]
    docks_graph_data.append(
        {'x': sub_df.index.values, 'y': sub_df['available_docks'].values,
         'type': 'bar', 'name': station}
    )

bikes_graph_data = []
for station in station_names:
    sub_df = grouped.loc[station]
    bikes_graph_data.append(
        {'x': sub_df.index.values, 'y': sub_df['available_bikes'].values,
         'type': 'bar', 'name': station}
    )

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': docks_graph_data,
            'layout': {
                'title': 'Available Docks'
            }
        }
    ),

    dcc.Graph(
        id='example-graph2',
        figure={
            'data': bikes_graph_data,
            'layout': {
                'title': 'Available Bikes'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
