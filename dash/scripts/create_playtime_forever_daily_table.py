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
cur_create.execute('''CREATE TABLE IF NOT EXISTS playtime_forever_daily
                    (steamid INTEGER, 
                    date TEXT,
                    appid INTEGER,
                    game_name TEXT,
                    playtime_forever
                    )''')

# Commit and close the database creation connection
conn_create.commit()
conn_create.close()

# Define function to fetch and process data
def get_playtime_data(steamid, name):
    response = api.call('IPlayerService.GetOwnedGames',
                        include_appinfo=True,
                        appids_filter=None,
                        include_extended_appinfo=False,
                        include_free_sub=False,
                        include_played_free_games=True,
                        steamid=steamid,
                        language='en')['response']['games']

    data = [{'steamid': steamid,
             'date': datetime.date.today(),
             'appid': int(game['appid']),  # Cast appid to int
             'game': game['name'],
             'playtime_forever': game['playtime_forever'] / 60}
            for game in response if game['playtime_forever'] > 0]

    return pd.DataFrame(data)

# Connect to the SQLite database for data retrieval
db_file = "dash\data\gametime.db"
conn = sqlite3.connect(db_file)
cur = conn.cursor()

# Query the 'users' table to get names and steamids
users_query = cur.execute('SELECT name, steamid FROM users')

# Fetch and process data for each user
playtime_data = [get_playtime_data(steamid, name) for name, steamid in users_query]

# Concatenate the dataframes and select only 'appid' and 'game' columns
playtime_forever_daily = pd.concat(playtime_data, axis=0).drop_duplicates()
playtime_forever_daily = playtime_forever_daily.sort_values(by='appid')
playtime_forever_daily['appid'] = playtime_forever_daily['appid'].astype(int)

# Insert data from the DataFrame into the 'games' table
playtime_forever_daily.to_sql('playtime_forever_daily', conn, if_exists='replace', index=False)

# Query and print data from the 'games' table
game_data = cur.execute("SELECT * FROM playtime_forever_daily ORDER BY appid, steamid").fetchall()
for row in game_data:
    print(row)

# Close the database connection
cur.close()
conn.close()

