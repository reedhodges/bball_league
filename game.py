import random
import numpy as np
from rosters import normalize_dict

# constants
TURNOVER_CHANCE = 0.05
ASSIST_CHANCE = 0.5
OFF_REBOUND_CHANCE_BASE = 0.25
OFF_REBOUND_BUFF_FACTOR = 0.25

def weighted_random_key(prob_dict):
    '''
    Pick a random key from a dictionary of probabilities.
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
        
def initialize_stats():
    '''
    Initializes a dictionary of stats for each position on a single posession.
    [PTS, REB, AST, 2PM, 2PA, 3PM, 3PA]
    '''
    return {pos: [0] * 7 for pos in ['PG', 'SG', 'SF', 'PF', 'C']}

def handle_shot(off_team, position, shot_worth, result):
    '''
    Determines if a shot is made and updates the stats accordingly.
    '''
    shot_key = 'fg2' if shot_worth == 2 else 'fg3'
    shot_chance = off_team.positions_dict[position].expected_stats[shot_key]
    if random.random() < shot_chance:
        # update points
        result[position][0] += shot_worth
        # update makes
        make_index = 3 if shot_worth == 2 else 5
        result[position][make_index] += 1
        return True
    # update misses
    miss_index = 4 if shot_worth == 2 else 6
    result[position][miss_index] += 1
    return False

def handle_assist(off_team, shooter, result):
    '''
    Determines if an assist is made and updates the stats accordingly.
    '''
    if random.random() < ASSIST_CHANCE:
        assister = weighted_random_key(off_team.ast_distribution_pos)
        while assister == shooter:
            assister = weighted_random_key(off_team.ast_distribution_pos)
        result[assister][2] += 1

def handle_rebound(team, result):
    '''
    Determines if a rebound is made and updates the stats accordingly.
    '''
    rebounder = weighted_random_key(team.reb_distribution_pos)
    result[rebounder][1] += 1

def possession(off_team, def_team):
    '''
    Simulates a possession and returns the players' stats.
    '''
    # initialize who will have the ball on the next possession
    next_team = def_team
    # initialize stats for this possession
    off_result, def_result = initialize_stats(), initialize_stats()

    # check for a turnover
    if random.random() < TURNOVER_CHANCE:
        return off_result, def_result, next_team
    
    # determine who will shoot the ball
    shooter = weighted_random_key(off_team.shot_distribution_pos)
    # decide whether they attempt a two or a three
    shooting_percentages = {2: off_team.positions_dict[shooter].expected_stats['fg2'], 3: off_team.positions_dict[shooter].expected_stats['fg3']}
    shooting_percentages = normalize_dict(shooting_percentages)
    shot_worth = weighted_random_key(shooting_percentages)

    # check for a made shot
    if handle_shot(off_team, shooter, shot_worth, off_result):
        handle_assist(off_team, shooter, off_result)
        return off_result, def_result, next_team
    
    # check for offensive rebound
    if random.random() < OFF_REBOUND_CHANCE_BASE + OFF_REBOUND_BUFF_FACTOR * ((off_team.expected_reb / def_team.expected_reb) - 1):
        handle_rebound(off_team, off_result)
        next_team = off_team
    # assign defensive rebound
    else:
        handle_rebound(def_team, def_result)
    
    return off_result, def_result, next_team
        
class game:
    '''
    Simulates a game by simulating a number of possessions between two teams.
    '''
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def initialize_box_score(self):
        return {pos: [0] * 7 for pos in ['PG', 'SG', 'SF', 'PF', 'C', 'Team']}

    def update_box_score(self, box_score, position_stats):
        for position, stats in position_stats.items():
            for i in range(7):
                box_score[position][i] += stats[i]

    def sum_team_stats(self, box_score):
        for i in range(7):
            box_score['Team'][i] = sum(stats[i] for position, stats in box_score.items() if position != 'Team')

    def play_game(self):
        team1_box_score = self.initialize_box_score()
        team2_box_score = self.initialize_box_score()

        num_possessions = int(np.ceil(sum([self.team1.pace, self.team2.pace]) / 2.0))

        off_team, def_team = self.team1, self.team2
        for _ in range(num_possessions * 2):
            off_result, def_result, next_team = possession(off_team, def_team)

            if off_team == self.team1:
                self.update_box_score(team1_box_score, off_result)
                self.update_box_score(team2_box_score, def_result)
            else:
                self.update_box_score(team2_box_score, off_result)
                self.update_box_score(team1_box_score, def_result)

            off_team, def_team = next_team, self.team1 if next_team == self.team2 else self.team2

        self.sum_team_stats(team1_box_score)
        self.sum_team_stats(team2_box_score)

        return team1_box_score, team2_box_score


#team1 = team('Team 1', seed=1)
#team2 = team('Team 2', seed=2)

#g1 = game(team1, team2)
#print(g1.play_game())