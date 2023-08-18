from datetime import date

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
from steam.webapi import WebAPI

import dash
from dash import Input, Output, dcc, html

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

load_figure_template("CYBORG")

df = pd.read_csv('dash\data\data.csv')

# Create a bar chart with data labels above the bars
fig = px.bar(df, x='date', y='difference', color='id', title='Playtime Per Day')

# Update y-axis label
fig.update_yaxes(title_text='Hours Played')

# Add data labels above the bars
fig.update_traces(
    texttemplate='%{text}',
    textposition='inside',
    text=df['difference'].fillna(0).astype(int),
    showlegend=False,
    textfont=dict(size=20, color='white')  # Set font size and color
)

# Calculate the rolling sum of the last 7 values of the 'difference' column
rolling_sum_7_days = df['difference'].rolling(window=7).sum().fillna(0).astype(int)

# Define the layout with improved styling
app.layout = html.Div([
    html.Div(
        [
            html.H1("Call of Duty: Modern Warfare II Stat Tracker", className="display-4"),
            html.P(id='data-as-of', className="lead")
        ],
        className="jumbotron"
    ),
    dcc.Graph(figure=fig, config={'displayModeBar': False}),
    html.Div(
        [
            html.H2(f"Total Playtime Over the Last 7 Days: {rolling_sum_7_days.iloc[-1]} hours"),
        ],
        className="mt-4"
    )
], className="container")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
