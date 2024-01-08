import numpy as np
import random
from datetime import datetime, timedelta

class player:
    '''
    Generates a player of a given position and sets their expected stats.
    '''
    def __init__(self, typical_stats, seed=None):
        self.expected_stats = {}
        self.seed = seed
        means_stds = {key: value for key, value in typical_stats.items() if type(value) == tuple} 
        poissons = {key: value for key, value in typical_stats.items() if type(value) == float}

        for stat, (mean, std) in means_stds.items():
            self.expected_stats[stat] = np.random.normal(mean, std, 1)[0]

        for stat, mean in poissons.items():
            self.expected_stats[stat] = np.random.poisson(mean, 1)[0]

        self.expected_stats['dob'] = weighted_random_date(datetime(1985, 1, 1), datetime(2004, 1, 1))
        self.expected_stats['handedness'] = 'L' if random.random() < 0.1 else 'R'

class guard(player):
    def __init__(self, seed=None):
        super().__init__({
            # stat: (mean, std)
            'fg2': (0.47, 0.09),
            'fg3': (0.35, 0.09),
            'height': (190, 9),
            'weight': (88, 5),
            # mean value 
            'dreb': 3.07,
            'oreb': 0.69,
            'ast': 4.6,
            'stl': 1.15,
            'blk': 0.29,
            'to': 2.12
        }, seed=seed)
        
class forward(player):
    def __init__(self, seed=None):
        super().__init__({
            # stat: (mean, std)
            'fg2': (0.49, 0.10),
            'fg3': (0.34, 0.09),
            'height': (200, 9),
            'weight': (100, 10),
            # mean value
            'dreb': 4.70,
            'oreb': 1.49,
            'ast': 2.33,
            'stl': 0.95,
            'blk': 0.67,
            'to': 1.68
        }, seed=seed+2)

class center(player):
    def __init__(self, seed=None):
        super().__init__({
            # stat: (mean, std)
            'fg2': (0.53, 0.10),
            'fg3': (0.32, 0.12),
            'height': (208, 9),
            'weight': (112, 10),
            # mean value 
            'dreb': 5.62,
            'oreb': 2.49,
            'ast': 1.62,
            'stl': 0.68,
            'blk': 1.24,
            'to': 1.60
        }, seed=seed+4)

def normalize_dict(dictionary):
    '''
    Normalize a dictionary of values so that they sum to 1.
    '''
    total = sum(dictionary.values())
    if total == 0:
        return {key: 0.2 for key in dictionary.keys()}
    return {key: value / total for key, value in dictionary.items()}

class team:
    ''' 
    Generates a team of 5 players.  Also sets the expected distribution of stats and the pace.
    '''
    def __init__(self, name, seed=None):
        self.name = name
        self.seed = seed
        # roster
        self.pg = guard(seed=self.seed)
        self.sg = guard(seed=self.seed + 1)
        self.sf = forward(seed=self.seed)
        self.pf = forward(seed=self.seed + 1)
        self.c = center(seed=self.seed)

        # dictionaries with position objects
        self.positions_dict = {
            'PG': self.pg,
            'SG': self.sg,
            'SF': self.sf,
            'PF': self.pf,
            'C': self.c
        }

        def roster_weight(stat_to_consider):
            # returns a dictionary of weights for each position based on a given stat.
            weights_dict = {}
            if stat_to_consider == 'fg':
                for position, player in self.positions_dict.items():
                    # choose the larger of 2P% and 3P%
                    weights_dict[position] = max(player.expected_stats['fg2'], player.expected_stats['fg3'])
                return normalize_dict(weights_dict)
            for position, player in self.positions_dict.items():
                weights_dict[position] = player.expected_stats[stat_to_consider]
            return normalize_dict(weights_dict)

        # expected distributions of stats by position
        self.shot_distribution_pos = roster_weight('fg')
        self.dreb_distribution_pos = roster_weight('dreb')
        self.oreb_distribution_pos = roster_weight('oreb')
        self.ast_distribution_pos = roster_weight('ast')
        self.stl_distribution_pos = roster_weight('stl')
        self.blk_distribution_pos = roster_weight('blk')
        self.to_distribution_pos = roster_weight('to')
        # pace of team: average number of possessions per game
        self.pace = np.random.normal(75, 5, 1)[0]
        # expected rebounds a team gets per game
        self.expected_dreb = sum(player.expected_stats['dreb'] for player in self.positions_dict.values())
        self.expected_oreb = sum(player.expected_stats['oreb'] for player in self.positions_dict.values())

def weighted_random_date(start_date, end_date):
    '''
    Picks a random date between start_date and end_date, with a higher probability of picking a date closer to end_date.
    '''
    delta = end_date - start_date
    weights = [i for i in range(delta.days + 1)]
    total_weight = sum(weights)
    chosen_weight = random.uniform(0, total_weight)
    cumulative_weight = 0
    for i, weight in enumerate(weights):
        cumulative_weight += weight
        if cumulative_weight >= chosen_weight:
            return start_date + timedelta(days=i)