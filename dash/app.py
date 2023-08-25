from datetime import date

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
from steam.webapi import WebAPI

import dash
from dash import Input, Output, dcc, html

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

load_figure_template("SUPERHERO")

# Read CSV data from GitHub repository
csv_url = 'https://raw.githubusercontent.com/ajhalling/mwii-time-tracker/main/dash/data/data.csv'
df = pd.read_csv(csv_url)

df = df[df['id']==76561198044737410]
df['date'] = pd.to_datetime(df['date'])

df.drop(columns='id', inplace=True)

# Filter data for the past 14 days
today = date.today()
two_weeks_ago = today - pd.DateOffset(days=14)
filtered_df = df[df['date'] >= two_weeks_ago]

# Create a bar chart with rotated date labels and filtered data
fig = px.bar(
    filtered_df, 
    x='date', 
    y='difference', 
    color='difference', 
    title='Playtime Per Day'
)

# Update the color scale title to an empty string
fig.update_layout(coloraxis_colorbar_title='', coloraxis_colorbar_xanchor='left')

# Update y-axis label
fig.update_yaxes(title_text='Hours Played')

# Rotate x-axis date labels by 90 degrees
fig.update_xaxes(tickangle=45)

# Get the list of all dates within the filtered range
all_dates = pd.date_range(start=two_weeks_ago, end=today, freq='D')

# Set tick mode to 'array' and provide tick values for all dates
fig.update_xaxes(
    tickmode='array',
    tickvals=all_dates,
    tickformat='%m-%d'  # Format as month-day
)

# Add data labels above the bars
fig.update_traces(
    texttemplate='%{text}',
    textposition='inside',
    text=filtered_df['difference'].fillna(0).astype(int),
    showlegend=False,
    textfont=dict(size=20, color='white')
)

# Calculate the rolling sum of the last 7 values of the 'difference' column
rolling_sum_7_days = df['difference'].rolling(window=7).sum().fillna(0).astype(int)

# Calculate the rolling sum of the last 7 values of the 'difference' column
rolling_sum_14_days = df['difference'].rolling(window=14).sum().fillna(0).astype(int)

# Define the layout with improved styling
app.layout = html.Div([
    html.Div(
        [
            html.H2("It's Gamer Time", className="display-4"),
            html.H3(f"Last 7 Days: {rolling_sum_7_days.iloc[-1]} hours", className="lead"),
            html.H3(f"Last 14 Days: {rolling_sum_14_days.iloc[-1]} hours", className="lead"),
        ],
        className="jumbotron"
    ),
    dcc.Graph(figure=fig, config={'displayModeBar': False}),
], className="container")


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
