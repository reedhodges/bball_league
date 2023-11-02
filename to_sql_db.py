import numpy as np
import sqlite3
from season import season

s = season(30)
s.play_season()
data = s.stats

# connect to database
conn = sqlite3.connect('game_stats.db')
c = conn.cursor()

# create table
c.execute('''CREATE TABLE IF NOT EXISTS game_stats
             (team INTEGER, game INTEGER, position INTEGER, stat INTEGER, value REAL)''')

# flatten array first
entries = []
for team in range(data.shape[0]):
    for game in range(data.shape[1]):
        for position in range(data.shape[2]):
            for stat in range(data.shape[3]):
                entries.append((team, game, position, stat, data[team, game, position, stat]))

# insert data in batches
batch_size = 1000
for i in range(0, len(entries), batch_size):
    c.executemany('INSERT INTO game_stats (team, game, position, stat, value) VALUES (?, ?, ?, ?, ?)', entries[i:i+batch_size])

# commit changes
conn.commit()

# close connection
conn.close()
