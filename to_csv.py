import pandas as pd
from season import season

s = season(30)
s.play_season()
data = s.stats

# flatten array first
entries = []
for team in range(data.shape[0]):
    for game in range(data.shape[1]):
        for position in range(data.shape[2]):
            for stat in range(data.shape[3]):
                entries.append((team, game, position, stat, data[team, game, position, stat]))

# convert to dataframe
df = pd.DataFrame(entries, columns=['team', 'game', 'position', 'stat', 'value'])
# remove rows whos stat is zero
df = df[df.value != 0.0]
df.to_csv('game_stats.csv', index=False)


