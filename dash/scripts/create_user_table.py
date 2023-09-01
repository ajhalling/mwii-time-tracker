import sqlite3

# Connect/create database
db_file = "dash\data\gametime.db"
conn = sqlite3.connect(db_file)
cur = conn.cursor()

# Create a User Profile table
# cur.execute('''CREATE TABLE IF NOT EXISTS users
#                 (steamid INTEGER , name TEXT)''')

# Test data
# user_list = [
#     (76561198044737410, 'Dickson'), 
#     (76561198037729598, 'AJ'), 
#     (76561198102561840, 'Ashton')
# ]

# Insert data into database
# cur.executemany('''
#         INSERT INTO users (steamid, name) VALUES (?, ?)
# ''', user_list)
# conn.commit()

user_data = cur.execute("SELECT * FROM users ORDER BY steamid")
for row in user_data:
    print(row)



# Close
cur.close()
conn.close()