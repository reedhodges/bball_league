import random
from rosters import team
import numpy as np

def weighted_random_key(prob_dict):
    '''
    Function to pick a random key from a dictionary of probabilities.
    '''
    # generate a random number
    rand_num = random.random()
    cumulative_probability = 0.0

    # iterate through the dictionary
    for key, probability in prob_dict.items():
        cumulative_probability += probability
        # check if the random number is less than the cumulative probability
        if rand_num < cumulative_probability:
            return key

def possession(off_team, def_team):
    # initialize who will have the ball on the next possession
    next_team = def_team
    # initialize stats for this possession
    off_possession_result = {
        # [PTS, REB, AST, 2PM, 2PA, 3PM, 3PA]
        'PG': [0, 0, 0, 0, 0, 0, 0],
        'SG': [0, 0, 0, 0, 0, 0, 0],
        'SF': [0, 0, 0, 0, 0, 0, 0],
        'PF': [0, 0, 0, 0, 0, 0, 0],
        'C': [0, 0, 0, 0, 0, 0, 0]
    }
    def_possession_result = {
        # [PTS, REB, AST, 2PM, 2PA, 3PM, 3PA]
        'PG': [0, 0, 0, 0, 0, 0, 0],
        'SG': [0, 0, 0, 0, 0, 0, 0],
        'SF': [0, 0, 0, 0, 0, 0, 0],
        'PF': [0, 0, 0, 0, 0, 0, 0],
        'C': [0, 0, 0, 0, 0, 0, 0]
    }
    # team will turn over the ball 5% of the time
    random_turnover = random.random()
    if random_turnover < 0.05:
        return off_possession_result, def_possession_result, next_team
    # pick a player to take the shot according to the team's distribution
    random_player = weighted_random_key(off_team.shot_distribution_pos)
    # split the string random_player into the position and shot worth
    position, shot_worth = random_player.split('_')
    shot_worth = int(shot_worth)
    # add the shot to the attempts
    if shot_worth == 2:
        off_possession_result[position][4] += 1
        # get the shot chance for the shot
        shot_chance = off_team.positions_dict[position].expected_stats['fg2']
    else:
        off_possession_result[position][6] += 1
        # get the shot chance for the shot
        shot_chance = off_team.positions_dict[position].expected_stats['fg3']
    # pick a random number to determine if the shot is made
    random_shot = random.random()
    # case where the shot is made
    if random_shot < shot_chance:
        # add points to the player's stats
        off_possession_result[position][0] += shot_worth
        # keep track of makes
        if shot_worth == 2:
            off_possession_result[position][3] += 1
        else:
            off_possession_result[position][5] += 1
        # check if assist is made
        ast_chance = random.random()
        if ast_chance < 0.5:
            # pick a random player to get the assist
            assister = weighted_random_key(off_team.ast_distribution_pos)
            # if the assister is the same as the shooter, pick a new one
            while assister == random_player:
                assister = weighted_random_key(off_team.ast_distribution_pos)
            # add the assist to the player's stats
            off_possession_result[assister][2] += 1
        return off_possession_result, def_possession_result, next_team
    # case where the shot is missed
    # allow for chance of offensive rebound
    off_reb_chance = random.random() 
    # case where there is an offensive rebound
    # give a buff based on how good the team is at rebounding
    if off_reb_chance < 0.25 + 0.25*((off_team.expected_reb / def_team.expected_reb) - 1):
        # pick a random player to get the rebound
        random_player = weighted_random_key(off_team.reb_distribution_pos)
        # add the rebound to the player's stats
        off_possession_result[random_player][1] += 1
        # change who will have the ball on the next possession
        next_team = off_team
        return off_possession_result, def_possession_result, next_team
    # case where there is no offensive rebound
    random_player = weighted_random_key(def_team.reb_distribution_pos)
    # add the rebound to the player's stats
    off_possession_result[random_player][1] += 1
    return off_possession_result, def_possession_result, next_team

class game:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def play_game(self):
        # initialize the box score for each team
        team1_box_score = {
            'PG': [0, 0, 0, 0, 0, 0, 0],
            'SG': [0, 0, 0, 0, 0, 0, 0],
            'SF': [0, 0, 0, 0, 0, 0, 0],
            'PF': [0, 0, 0, 0, 0, 0, 0],
            'C': [0, 0, 0, 0, 0, 0, 0]
        }
        team2_box_score = {
            'PG': [0, 0, 0, 0, 0, 0, 0],
            'SG': [0, 0, 0, 0, 0, 0, 0],
            'SF': [0, 0, 0, 0, 0, 0, 0],
            'PF': [0, 0, 0, 0, 0, 0, 0],
            'C': [0, 0, 0, 0, 0, 0, 0]
        }

        # compute number of possessions for each team: average of paces
        num_possessions = int(np.ceil(sum([self.team1.pace, self.team2.pace]) / 2.0))

        # initialize offensive and defensive teams
        off_team = self.team1
        def_team = self.team2
        for _ in range(num_possessions*2):
            off_result, def_result, next_team = possession(off_team, def_team)
            # add the results to the box score
            if off_team == self.team1:
                for position, stats in off_result.items():
                    for i in range(7):
                        team1_box_score[position][i] += stats[i]
                for position, stats in def_result.items():
                    for i in range(7):
                        team2_box_score[position][i] += stats[i]
            else:
                for position, stats in off_result.items():
                    for i in range(7):
                        team2_box_score[position][i] += stats[i]
                for position, stats in def_result.items():
                    for i in range(7):
                        team1_box_score[position][i] += stats[i]
            # switch the offensive and defensive teams
            off_team = next_team
            if off_team == self.team1:
                def_team = self.team2
            else:
                def_team = self.team1
        # sum the results for the team and add to the dictionaries
        team1_box_score['Team'] = [sum([stats[i] for stats in team1_box_score.values()]) for i in range(7)]
        team2_box_score['Team'] = [sum([stats[i] for stats in team2_box_score.values()]) for i in range(7)]
        return team1_box_score, team2_box_score

#team1 = team('Team 1', seed=1)
#team2 = team('Team 2', seed=2)

#g1 = game(team1, team2)
#print(g1.play_game())