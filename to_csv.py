import pandas as pd
from season import season
from math import trunc

s = season(30)
game_data = s.stats

# create flattened array with team ID, game ID, position ID, PTS, REB, AST columns
entries = []
for team in range(game_data.shape[0]):
    for game in range(game_data.shape[1]):
        for position in range(game_data.shape[2]):
            entries.append((team, game, position, game_data[team, game, position, 0], game_data[team, game, position, 1], game_data[team, game, position, 2]))

# convert to dataframe
df_stats = pd.DataFrame(entries, columns=['team_id', 'game_id', 'pos_id', 'PTS', 'REB', 'AST'])
# remove rows whos stats are all zero
df_stats = df_stats[(df_stats.PTS != 0.0) | (df_stats.REB != 0.0) | (df_stats.AST != 0.0)]
# add a new column for team name
df_stats['team_name'] = df_stats.team_id.apply(lambda x: s.teams[x].name)
# add a new column for position name
df_stats['pos_name'] = df_stats.pos_id.apply(lambda x: s.positions[x])
# add a new column for player ID that is a combination of team ID and position ID, converted to int
df_stats['player_id'] = df_stats.apply(lambda x: int(str(x.team_id) + str(x.pos_id)), axis=1)

# save as csv
df_stats.to_csv('game_stats.csv', index=False)

# now make a dataframe with for team stats
# columns: team ID, team name, wins, losses, draws
entries = []
for team in range(s.num_teams):
    entries.append((team,s.teams[team].name, trunc(s.team_stats[team, 0]), trunc(s.team_stats[team, 1]), trunc(s.team_stats[team, 2])))
df_team_stats = pd.DataFrame(entries, columns=['team_id','team', 'W', 'L', 'D'])
df_team_stats.to_csv('team_stats.csv', index=False)

# now make a dataframe with player attributes from dictionary
# columns: player ID, team ID, team name, position ID, position name, all attributes
entries = []
for team in range(s.num_teams):
    for position in range(len(s.positions)):
        entries.append((int(str(team) + str(position)), team, s.teams[team].name, position, s.positions[position], *s.teams[team].__dict__[s.positions[position]].attributes.values(),s.teams[team].__dict__[s.positions[position]].overall))
# convert to dataframe
df_attributes = pd.DataFrame(entries, columns=['player_id', 'team_id', 'team_name', 'pos_id', 'pos_name', 'outside_scoring', 'inside_scoring', 'defending', 'athleticism', 'playmaking', 'rebounding', 'intangibles', 'height', 'overall'])
# save as csv
df_attributes.to_csv('player_attributes.csv', index=False)