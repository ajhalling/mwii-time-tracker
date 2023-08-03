import pathlib
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_table
from steam.webapi import WebAPI
from datetime import date, timedelta

app = Dash(__name__, title="codtime")

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

API_KEY = '757E46884546DBD5C0B5FF849A3842A4'

api = WebAPI(API_KEY, raw=False, format='json', https=True, http_timeout=10)

def mw2_playtime_hours(steamids):
    data = api.call('IPlayerService.GetOwnedGames', appids_filter=['1938090'], include_appinfo=True, include_extended_appinfo=True, include_free_sub=True, include_played_free_games=True, steamid=steamids, language='en')
    return data['response']['games'][0]['playtime_forever']/60

def load_data(data_file: str) -> pd.DataFrame:
    '''
    Load data from /data directory
    '''
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(data_file))

def add_new_row(df):
    # Get today's date
    today = date.today().strftime('%Y-%m-%d')

    # Check if the max 'date' in the DataFrame is equal to today
    if df['date'].max() == today:
        return df

    # Get yesterday's date
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Get yesterday's playtime_total
    try:
        yesterday_playtime_total = df[df['date'] == yesterday]['playtime_total'].values[0]
    except:
        yesterday_playtime_total = 0.0

    # Get today's playtime_total
    today_playtime_total = mw2_playtime_hours('76561198044737410')

    # Calculate today's playtime_today
    playtime_today = today_playtime_total - yesterday_playtime_total

    # If playtime_today is NaN or below zero, set it to zero
    if pd.isna(playtime_today) or playtime_today < 0:
        playtime_today = 0.0

    # Create the new row
    new_row = pd.DataFrame({'date': [today], 'playtime_total': [today_playtime_total], 'playtime_today': [playtime_today]})

    # Concatenate the new row to the original DataFrame
    df = pd.concat([df, new_row], ignore_index=True)

    return df

# Read CSV with existing data
df = pd.read_csv('playtime.csv')

# Add a new row to the DataFrame
df = add_new_row(df)

# Save CSV
df.to_csv('playtime.csv', index=False)

# Define the layout of the app
app.layout = html.Div([
    html.H1("MWII Tracking"),
    dash_table.DataTable(
        id='data-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
    ),
    # Interval component to update the data every 12 hours
    dcc.Interval(
        id='update-interval',
        interval=12 * 60 * 60 * 1000,  # 12 hours in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('data-table', 'data'),
    [Input('update-interval', 'n_intervals')]
)
def update_data_table(n):
    # Read CSV with existing data
    df = pd.read_csv('playtime.csv')

    # Add a new row to the DataFrame
    df = add_new_row(df)

    # Save CSV
    df.to_csv('playtime.csv', index=False)

    return df.to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=True)
