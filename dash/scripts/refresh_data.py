import os
from datetime import date

import pandas as pd
from steam.webapi import WebAPI

API_KEY = os.environ['API_KEY']

api = WebAPI(API_KEY, raw=False, format='json', https=True, http_timeout=10)

def mw2_playtime_hours(steamids):
    data = api.call('IPlayerService.GetOwnedGames', appids_filter=['1938090'], include_appinfo=True, include_extended_appinfo=True, include_free_sub=True, include_played_free_games=True, steamid=steamids, language='en')
    return data['response']['games'][0]['playtime_forever']/60

ids = ['76561198044737410','76561198037729598','76561198102561840']

def add_new_rows(df, ids):

    today = date.today().strftime('%Y-%m-%d')

    new_rows = []

    for id in ids:
        playtime = mw2_playtime_hours(id)
        id_str = str(id)  # Rename 'id' variable to 'id_str' to avoid conflict
        new_row = pd.DataFrame({'date': [today], 'id': id_str, 'playtime_total': [playtime]})  # Remove extra brackets around 'id_str'
        new_rows.append(new_row)

    if df['date'].eq(today).any():
        print(f"Rows for {today} already exist in DataFrame. Updating playtime_total.")
        for nr in new_rows:
            df.loc[(df['date'] == today) & (df['id'] == nr['id'].iloc[0]), 'playtime_total'] = nr['playtime_total'].iloc[0]
    else:
        print(f"Adding {len(new_rows)} rows for {ids}")
        df = pd.concat([df] + new_rows, ignore_index=True)

    return df

# Read CSV with existing data
df = pd.read_csv('dash/data/data.csv')

# Add a new row to the DataFrame
df = add_new_rows(df, ids)

# Sort the data by 'id' and 'date'
df.sort_values(['id', 'date'], inplace=True)

# Calculate the difference between the previous bar with the same ID
df['difference'] = df.groupby('id')['playtime_total'].diff()

# Fill NaN values in the 'difference' column with 0
df['difference'].fillna(0, inplace=True)

# Save CSV
df.to_csv('dash/data/data.csv', index=False)