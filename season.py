import numpy as np
import pandas as pd
from itertools import combinations
from math import comb
from datetime import timedelta, datetime
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
        self.df_player_info = self.initialize_player_info_df()
        self.team_records = {team_name: [0, 0, 0] for team_name in team_nicknames[:self.num_teams]}
        # initialize date the last time each team played a game to the start of the season
        self.team_last_game_date = {team_name: datetime(2024, 1, 1) for team_name in team_nicknames[:self.num_teams]}


    def generate_matchups(self):
        matchups = np.array(list(combinations(self.teams, 2)))
        # flip the matchups so that each team plays each other team twice
        return np.concatenate((matchups, np.flip(matchups, axis=1)))

    def initialize_game_stats_df(self):
        columns = ['GAME_ID', 'GAME_DATE', 'TEAM_NAME', 'OPPONENT_NAME', 'PLAYER_NAME', 'POSITION', 'PTS', 'DREB', 'OREB', 'AST', 'FG2M', 'FG2A', 'FG3M', 'FG3A', 'STL', 'BLK', 'TO']
        return pd.DataFrame(columns=columns)
    
    def initialize_player_info_df(self):
        columns = ['PLAYER_NAME', 'HEIGHT', 'WEIGHT', 'DOB', 'HANDEDNESS']
        return pd.DataFrame(columns=columns)

    def add_game_stats(self, game_id, game_date, team, opponent, team_stats):
        # add the team stats for a single game to the game stats dataframe
        rows = [[game_id, game_date, team.name, opponent.name, f"{team.name}_{position}", position] + stats for position, stats in team_stats.items()]
        self.df_game_stats = pd.concat([self.df_game_stats, pd.DataFrame(rows, columns=self.df_game_stats.columns)], ignore_index=True)

    def add_player_info(self, team):
        # add the player info for a single team to the player info dataframe
        rows = [
            [
                f"{team.name}_{position}", 
                player.expected_stats['height'], 
                player.expected_stats['weight'], 
                player.expected_stats['dob'], 
                player.expected_stats['handedness']
            ] 
            for position, player in team.positions_dict.items()
        ]
        self.df_player_info = pd.concat([self.df_player_info, pd.DataFrame(rows, columns=self.df_player_info.columns)], ignore_index=True)


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

    def assign_game_date(self, team1_name, team2_name):
        last_date_team1 = self.team_last_game_date[team1_name]
        last_date_team2 = self.team_last_game_date[team2_name]
        max_date = max(last_date_team1, last_date_team2)
        next_game_date = max_date + timedelta(days=2)
        self.team_last_game_date[team1_name] = next_game_date
        self.team_last_game_date[team2_name] = next_game_date
        return next_game_date

    def play_season(self):
        for game_id in range(self.num_games):
            team1, team2 = self.matchups[game_id]
            game_date = self.assign_game_date(team1.name, team2.name)
            team1_stats, team2_stats = game(team1, team2).play_game()
            self.add_game_stats(game_id, game_date, team1, team2, team1_stats)
            self.add_game_stats(game_id, game_date, team2, team1, team2_stats)
            self.update_team_records(team1, team2, team1_stats, team2_stats)

        for team in self.teams:
            self.add_player_info(team)

        self.team_records = {key: value for key, value in sorted(self.team_records.items(), key=lambda item: item[1][0], reverse=True)}

s = season(50)
s.play_season()
print(s.team_records)

# save the game stats to a csv file
s.df_game_stats.to_csv('game_stats.csv', index=False)
# save the player info to a csv file
s.df_player_info.to_csv('player_info.csv', index=False)