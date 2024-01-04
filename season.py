import numpy as np
import pandas as pd
from itertools import combinations
from math import comb
from game import game
from rosters import team
from lists import team_nicknames

class season:
    def __init__(self, num_teams):
        self.num_teams = num_teams
        self.num_games = 2*comb(self.num_teams, 2)
        
        # create list of teams
        self.teams = [team(name=team_nicknames[i], seed=i) for i in range(self.num_teams)]

        # create numpy array with all combinations of two teams
        self.matchups = np.array(list(combinations(self.teams, 2)))
        # redefine it with two of each matchup
        self.matchups = np.concatenate((self.matchups, np.flip(self.matchups, axis=1)))

        # initialize a pandas dataframe with game statistics by player
        self.df_game_stats = pd.DataFrame(columns= ['GAME_ID',
                                               'TEAM_NAME',
                                               'OPPONENT_NAME',
                                                'PLAYER_NAME',
                                                'POSITION',
                                                'PTS',
                                                'REB',
                                                'AST',
                                                'FG2M',
                                                'FG2A',
                                                'FG3M',
                                                'FG3A'
                                               ])
        
        # initialize dictionary of team records
        self.team_records = {key: [0, 0, 0] for key in team_nicknames[:self.num_teams]}

    def play_season(self):
        # play each game
        for i in range(self.num_games):
            # play the game
            team1, team2 = self.matchups[i]
            team1_stats, team2_stats = game(team1, team2).play_game()
            # initialize new rows of stats to add
            new_rows = []
            # add the stats to the game stats dataframe
            for key, value in team1_stats.items():
                new_rows.append([i, team1.name, team2.name, team1.name + '_' + key, key] + value)
            for key, value in team2_stats.items():
                new_rows.append([i, team2.name, team1.name, team2.name + '_' + key, key] + value)
            self.df_game_stats = pd.concat([self.df_game_stats, pd.DataFrame(new_rows, columns=self.df_game_stats.columns)], ignore_index=True)
            # update the team records
            if team1_stats['Team'][0] > team2_stats['Team'][0]:
                self.team_records[team1.name][0] += 1
                self.team_records[team2.name][1] += 1
            elif team1_stats['Team'][0] < team2_stats['Team'][0]:
                self.team_records[team1.name][1] += 1
                self.team_records[team2.name][0] += 1
            # case of a draw
            else:
                self.team_records[team1.name][2] += 1
                self.team_records[team2.name][2] += 1
        # sort the team records by wins
        self.team_records = {key: value for key, value in sorted(self.team_records.items(), key=lambda item: item[1][0], reverse=True)}

s = season(30)
s.play_season()
print(s.team_records)

# save the game stats to a csv file
s.df_game_stats.to_csv('game_stats.csv', index=False)