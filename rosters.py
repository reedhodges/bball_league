import numpy as np
import pandas as pd
from scipy.stats import truncnorm

# use a truncated normal distribution to generate a random
# skill rating between 0 and 100, for a given mean and std dev
def truncated_norm(mean, std_dev, seed=None):
    # make sure the seed is set so that the same player is generated
    if seed is not None:
        np.random.seed(seed)
    a = (0 - mean) / std_dev
    b = (100 - mean) / std_dev
    return truncnorm.rvs(a, b, loc=mean, scale=std_dev)

class Player:
    def __init__(self, attribute_means_and_stds, seed=None):
        self.attributes = {}
        for key, (mean, std) in attribute_means_and_stds.items():
            self.attributes[key] = truncated_norm(mean, std, seed)
        
        # Define overall to be the average of the top 3 attributes
        self.overall = np.mean(sorted(self.attributes.values())[-3:])
        
        # Define expected values of a player's stats
        self.pts = 0.1 * (self.attributes['outside_scoring'] + self.attributes['inside_scoring'])
        self.reb = 0.05 * self.attributes['rebounding']
        self.ast = 0.05 * self.attributes['playmaking']

class pg(Player):
    def __init__(self, seed=None):
        super().__init__({
            'outside_scoring': (80, 15),
            'inside_scoring': (60, 10),
            'defending': (70, 20),
            'athleticism': (80, 10),
            'playmaking': (85, 10),
            'rebounding': (60, 15),
            'intangibles': (70, 5)
        }, seed=seed)

class sg(Player):
    def __init__(self, seed=None):
        super().__init__({
            'outside_scoring': (85, 15),
            'inside_scoring': (60, 10),
            'defending': (70, 20),
            'athleticism': (80, 10),
            'playmaking': (75, 15),
            'rebounding': (60, 15),
            'intangibles': (70, 5)
        }, seed=seed)

class sf(Player):
    def __init__(self, seed=None):
        super().__init__({
            'outside_scoring': (75, 15),
            'inside_scoring': (75, 15),
            'defending': (75, 10),
            'athleticism': (60, 15),
            'playmaking': (60, 15),
            'rebounding': (75, 15),
            'intangibles': (70, 5)
        }, seed=seed)

class pf(Player):
    def __init__(self, seed=None):
        super().__init__({
            'outside_scoring': (60, 15),
            'inside_scoring': (80, 10),
            'defending': (75, 10),
            'athleticism': (70, 15),
            'playmaking': (60, 15),
            'rebounding': (80, 15),
            'intangibles': (70, 5)
        }, seed=seed)

class c(Player):
    def __init__(self, seed=None):
        super().__init__({
            'outside_scoring': (50, 15),
            'inside_scoring': (85, 15),
            'defending': (80, 10),
            'athleticism': (60, 10),
            'playmaking': (60, 15),
            'rebounding': (85, 5),
            'intangibles': (70, 5)
        }, seed=seed)

class team:
    def __init__(self, name, seed=None):
        self.name = name
        self.seed = seed
        # roster
        self.pg = pg(seed=self.seed)
        self.sg = sg(seed=self.seed)
        self.sf = sf(seed=self.seed)
        self.pf = pf(seed=self.seed)
        self.c = c(seed=self.seed)
        # overall rating
        self.overall = np.mean([self.pg.overall, self.sg.overall, self.sf.overall, self.pf.overall, self.c.overall])

        # expected stats
        self.pts = self.pg.pts + self.sg.pts + self.sf.pts + self.pf.pts + self.c.pts
        self.reb = self.pg.reb + self.sg.reb + self.sf.reb + self.pf.reb + self.c.reb
        self.ast = self.pg.ast + self.sg.ast + self.sf.ast + self.pf.ast + self.c.ast