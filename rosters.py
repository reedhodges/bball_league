import numpy as np

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

        # create an overall rating of each player based on their expected stats
        self.overall = (self.expected_stats['fg2'] + self.expected_stats['fg3']  + self.expected_stats['reb'] + self.expected_stats['ast']) / (typical_stats['fg2'][0] * typical_stats['fg3'][0] * typical_stats['reb'] * typical_stats['ast']) 
        

class guard(player):
    def __init__(self, seed=None):
        super().__init__({
            # stat: (mean, std)
            'fg2': (0.47, 0.09),
            'fg3': (0.35, 0.09),
            # mean value 
            'reb': 3.8,
            'ast': 4.6
        }, seed=seed)
        
class forward(player):
    def __init__(self, seed=None):
        super().__init__({
            # stat: (mean, std)
            'fg2': (0.49, 0.10),
            'fg3': (0.34, 0.09),
            # mean value
            'reb': 6.2,
            'ast': 2.3
        }, seed=seed+2)

class center(player):
    def __init__(self, seed=None):
        super().__init__({
            # stat: (mean, std)
            'fg2': (0.53, 0.10),
            'fg3': (0.32, 0.12),
            # mean value 
            'reb': 8.1,
            'ast': 1.6
        }, seed=seed+4)

def normalize_dict(dictionary):
    '''
    Normalize a dictionary of values so that they sum to 1.
    '''
    total = sum(dictionary.values())
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

        # expected distribution of shots taken by position
        self.shot_distribution_pos = roster_weight('fg')
        # expected distribution of rebounds by position
        self.reb_distribution_pos = roster_weight('reb')
        # expected distribution of assists by position
        self.ast_distribution_pos = roster_weight('ast')
        # pace of team: average number of possessions per game
        self.pace = np.random.normal(75, 5, 1)[0]
        # expected rebounds a team gets per game
        self.expected_reb = sum(player.expected_stats['reb'] for player in self.positions_dict.values())