'''
 # @ Create Time: 2023-08-02 21:46:33.197096
'''

import pathlib
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_table

app = Dash(__name__, title="codtime")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

def load_data(data_file: str) -> pd.DataFrame:
    '''
    Load data from /data directory
    '''
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(data_file))

df = load_data("playtime.csv")

# Define the layout of the app
app.layout = html.Div([
    html.H1("MWII Tracking"),
    dash_table.DataTable(
        id='data-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)


