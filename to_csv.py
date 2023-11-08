import pandas as pd
from season import season

s = season(30)
data = s.stats

# flatten array first
entries = []
for team in range(data.shape[0]):
    for game in range(data.shape[1]):
        for position in range(data.shape[2]):
            for stat in range(data.shape[3]):
                entries.append((team, game, position, stat, data[team, game, position, stat]))

# convert to dataframe
df_stats = pd.DataFrame(entries, columns=['team', 'game_id', 'pos', 'stat', 'val'])
# remove rows whos stat is zero
df_stats = df_stats[df_stats.val != 0.0]

# give teams, positions, stats a name
df_stats.team = df_stats.team.apply(lambda x: s.teams[x].name)
df_stats.pos = df_stats.pos.apply(lambda x: s.positions[x])
df_stats.stat = df_stats.stat.apply(lambda x: s.stat_names[x])

df_stats.to_csv('game_stats.csv', index=False)


