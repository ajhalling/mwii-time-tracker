import datetime
import os
import sqlite3
import pandas as pd
from steam.webapi import WebAPI

API_KEY = os.environ['API_KEY']

api = WebAPI(API_KEY, raw=False, format='json', https=True, http_timeout=10)

# Connect/create database
db_file = "dash\data\gametime.db"
conn_create = sqlite3.connect(db_file)
cur_create = conn_create.cursor()

# Create a games table with appid as INTEGER
cur_create.execute('''CREATE TABLE IF NOT EXISTS playtime (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    steamid INTEGER NOT NULL,
    appid INTEGER NOT NULL,
    play_date DATE NOT NULL,
    playtime_hours REAL NOT NULL,
    FOREIGN KEY (appid) REFERENCES games(appid),
    UNIQUE(steamid, appid, play_date)
)

                    ''')

# Commit and close the database creation connection
conn_create.commit()
conn_create.close()

