import numpy as np

class player:
    def __init__(self, typical_stats, seed=None):
        # initialize dictionary for expected stats
        self.expected_stats = {}
        # set random seed
        self.seed = seed
        # make a dictionary of means and stds
        means_stds = {key: value for key, value in typical_stats.items() if type(value) == tuple} 
        # make a dictionary of Poisson distributed stats
        poissons = {key: value for key, value in typical_stats.items() if type(value) == float}
        # pick random values from normal distribution for shooting percentages
        for stat, (mean, std) in means_stds.items():
            self.expected_stats[stat] = np.random.normal(mean, std, 1)[0]
        # pick random values from Poisson distribution for other stats
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

class team:
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

        # sum the expected FG2% and FG3% for each position
        self.expected_fg2 = self.pg.expected_stats['fg2'] + self.sg.expected_stats['fg2'] + self.sf.expected_stats['fg2'] + self.pf.expected_stats['fg2'] + self.c.expected_stats['fg2']
        self.expected_fg3 = self.pg.expected_stats['fg3'] + self.sg.expected_stats['fg3'] + self.sf.expected_stats['fg3'] + self.pf.expected_stats['fg3'] + self.c.expected_stats['fg3']
        self.expected_fg = self.expected_fg2 + self.expected_fg3

        # sum the expected rebounds for the team
        self.expected_reb = self.pg.expected_stats['reb'] + self.sg.expected_stats['reb'] + self.sf.expected_stats['reb'] + self.pf.expected_stats['reb'] + self.c.expected_stats['reb']

        # sum the expected assists for the team
        self.expected_ast = self.pg.expected_stats['ast'] + self.sg.expected_stats['ast'] + self.sf.expected_stats['ast'] + self.pf.expected_stats['ast'] + self.c.expected_stats['ast']

        # expected distribution of shots taken by position
        self.shot_distribution_pos = {
            'PG_2': self.pg.expected_stats['fg2'] / self.expected_fg,
            'PG_3': self.pg.expected_stats['fg3'] / self.expected_fg,
            'SG_2': self.sg.expected_stats['fg2'] / self.expected_fg,
            'SG_3': self.sg.expected_stats['fg3'] / self.expected_fg,
            'SF_2': self.sf.expected_stats['fg2'] / self.expected_fg,
            'SF_3': self.sf.expected_stats['fg3'] / self.expected_fg,
            'PF_2': self.pf.expected_stats['fg2'] / self.expected_fg,
            'PF_3': self.pf.expected_stats['fg3'] / self.expected_fg,
            'C_2': self.c.expected_stats['fg2'] / self.expected_fg,
            'C_3': self.c.expected_stats['fg3'] / self.expected_fg
        }

        # expected distribution of rebounds by position
        self.reb_distribution_pos = {
            'PG': self.pg.expected_stats['reb'] / self.expected_reb,
            'SG': self.sg.expected_stats['reb'] / self.expected_reb,
            'SF': self.sf.expected_stats['reb'] / self.expected_reb,
            'PF': self.pf.expected_stats['reb'] / self.expected_reb,
            'C': self.c.expected_stats['reb'] / self.expected_reb
        }

        # expected distribution of assists by position
        self.ast_distribution_pos = {
            'PG': self.pg.expected_stats['ast'] / self.expected_ast,
            'SG': self.sg.expected_stats['ast'] / self.expected_ast,
            'SF': self.sf.expected_stats['ast'] / self.expected_ast,
            'PF': self.pf.expected_stats['ast'] / self.expected_ast,
            'C': self.c.expected_stats['ast'] / self.expected_ast
        }

        # pace of team: average number of possessions per game
        self.pace = np.random.normal(75, 5, 1)[0]