import numpy as np
from itertools import combinations
from math import comb, trunc
from game import game
from rosters import team
from lists import team_nicknames

class season:
    def __init__(self, num_teams):
        self.num_teams = num_teams
        self.num_games = 2*comb(self.num_teams, 2)
        
        # Create teams
        self.teams = [team(name=team_nicknames[i],seed=i) for i in range(self.num_teams)]

        # Create numpy array with all combinations of two teams
        self.matchups = np.array(list(combinations(self.teams, 2)))
        # redefine it with two of each matchup
        self.matchups = np.concatenate((self.matchups, np.flip(self.matchups, axis=1)))

        # initialize stats for the league
        self.stats = np.zeros((self.num_teams,self.num_games,5,3))

        # initialize win-loss record for each team
        self.team_stats = np.zeros((self.num_teams,3))

    def play_season(self):
        # iterate over each matchup
        for i in range(self.num_games):
            # create a game instance
            g = game(self.matchups[i,0], self.matchups[i,1], i, self.stats, self.team_stats)
            # calculate box scores for both teams
            g.calculate_box_score(self.matchups[i,0], 1)
            g.calculate_box_score(self.matchups[i,1], -1)
            g.win_loss()

    # print a stat for a specific team, game, position, and stat
    def return_stats(self, team, game, pos, stat):
        self.play_season()
        return self.stats[team, game, pos, stat]

    # Print team names used in this instance
    def print_teams(self):
        for i in range(len(self.teams)):
            print(self.teams[i].name)

    # print a table of league standings
    def standings(self):
        self.play_season()
    
        # Combine team names with their stats for sorting
        team_standings = [(self.teams[i].name, *self.team_stats[i]) for i in range(len(self.teams))]
    
        # Sort the combined list by wins (which is the first element of the stats tuple)
        sorted_standings = sorted(team_standings, key=lambda x: x[1], reverse=True)
    
        # Print standings
        for team_name, wins, losses, ties in sorted_standings:
            print(f"{team_name}: {trunc(wins)}-{trunc(losses)}-{trunc(ties)}")

    # print a table of league leaders
    def league_leaders(self):
        self.play_season()
        positions = ['PG', 'SG', 'SF', 'PF', 'C']
        # compute the average stats for each player
        average_stats = np.sum(self.stats, axis=1) / (2.*self.num_teams - 2.)

        # make 2d arrays for each stat
        ppg = average_stats[:,:,0]
        rpg = average_stats[:,:,1]
        apg = average_stats[:,:,2]

        # find the max of each stat
        ppg_indices = np.unravel_index(np.argmax(ppg), ppg.shape)
        ppg_team_index, ppg_pos_index = ppg_indices
        rpg_indices = np.unravel_index(np.argmax(rpg), rpg.shape)
        rpg_team_index, rpg_pos_index = rpg_indices
        apg_indices = np.unravel_index(np.argmax(apg), apg.shape)
        apg_team_index, apg_pos_index = apg_indices

        # print the results
        print(f"PTS leader: {self.teams[ppg_team_index].name} {positions[ppg_pos_index]}, {round(ppg[ppg_indices],1)} PPG")
        print(f"REB leader: {self.teams[rpg_team_index].name} {positions[rpg_pos_index]}, {round(rpg[rpg_indices],1)} RPG")
        print(f"AST leader: {self.teams[apg_team_index].name} {positions[apg_pos_index]}, {round(apg[apg_indices],1)} APG")

s = season(30)
s.standings()
print()
s.league_leaders()