import pandas as pd
from season import season
from math import trunc

s = season(30)
game_data = s.stats

# flatten array first
entries = []
for team in range(game_data.shape[0]):
    for game in range(game_data.shape[1]):
        for position in range(game_data.shape[2]):
            for stat in range(game_data.shape[3]):
                entries.append((team, game, position, stat, game_data[team, game, position, stat]))

# convert to dataframe
df_stats = pd.DataFrame(entries, columns=['team', 'game_id', 'pos', 'stat', 'val'])
# remove rows whos stat is zero
df_stats = df_stats[df_stats.val != 0.0]

# give teams, positions, stats a name
df_stats.team = df_stats.team.apply(lambda x: s.teams[x].name)
df_stats.pos = df_stats.pos.apply(lambda x: s.positions[x])
df_stats.stat = df_stats.stat.apply(lambda x: s.stat_names[x])

df_stats.to_csv('game_stats.csv', index=False)

# now make a dataframe with for team stats
# columns: team name, wins, losses, draws
entries = []
for team in range(s.num_teams):
    entries.append((s.teams[team].name, trunc(s.team_stats[team, 0]), trunc(s.team_stats[team, 1]), trunc(s.team_stats[team, 2])))
df_team_stats = pd.DataFrame(entries, columns=['team', 'W', 'L', 'D'])
df_team_stats.to_csv('team_stats.csv', index=False)


