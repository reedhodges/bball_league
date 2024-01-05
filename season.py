import numpy as np
import pandas as pd
from itertools import combinations
from math import comb
from game import game
from rosters import team
from lists import team_nicknames

class season:
    '''
    Simulates a season by simulating all games between all teams.  Each team plays every other team twice.
    '''
    def __init__(self, num_teams):
        self.num_teams = num_teams
        self.num_games = 2 * comb(self.num_teams, 2)
        self.teams = [team(name=team_nicknames[i], seed=i) for i in range(self.num_teams)]
        self.matchups = self.generate_matchups()
        self.df_game_stats = self.initialize_game_stats_df()
        self.team_records = {team_name: [0, 0, 0] for team_name in team_nicknames[:self.num_teams]}

    def generate_matchups(self):
        matchups = np.array(list(combinations(self.teams, 2)))
        # flip the matchups so that each team plays each other team twice
        return np.concatenate((matchups, np.flip(matchups, axis=1)))

    def initialize_game_stats_df(self):
        columns = ['GAME_ID', 'TEAM_NAME', 'OPPONENT_NAME', 'PLAYER_NAME', 'POSITION', 'PTS', 'DREB', 'OREB', 'AST', 'FG2M', 'FG2A', 'FG3M', 'FG3A', 'STL', 'BLK', 'TO']
        return pd.DataFrame(columns=columns)

    def add_game_stats(self, game_id, team, opponent, team_stats):
        # add the team stats for a single game to the game stats dataframe
        rows = [[game_id, team.name, opponent.name, f"{team.name}_{position}", position] + stats for position, stats in team_stats.items()]
        self.df_game_stats = pd.concat([self.df_game_stats, pd.DataFrame(rows, columns=self.df_game_stats.columns)], ignore_index=True)

    def update_team_records(self, team1, team2, team1_stats, team2_stats):
        if team1_stats['Team'][0] > team2_stats['Team'][0]:
            self.team_records[team1.name][0] += 1
            self.team_records[team2.name][1] += 1
        elif team1_stats['Team'][0] < team2_stats['Team'][0]:
            self.team_records[team1.name][1] += 1
            self.team_records[team2.name][0] += 1
        else:
            self.team_records[team1.name][2] += 1
            self.team_records[team2.name][2] += 1

    def play_season(self):
        for game_id in range(self.num_games):
            team1, team2 = self.matchups[game_id]
            team1_stats, team2_stats = game(team1, team2).play_game()
            self.add_game_stats(game_id, team1, team2, team1_stats)
            self.add_game_stats(game_id, team2, team1, team2_stats)
            self.update_team_records(team1, team2, team1_stats, team2_stats)

        self.team_records = {key: value for key, value in sorted(self.team_records.items(), key=lambda item: item[1][0], reverse=True)}

s = season(100)
s.play_season()
print(s.team_records)

# save the game stats to a csv file
s.df_game_stats.to_csv('game_stats.csv', index=False)