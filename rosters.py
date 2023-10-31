import numpy as np
import pandas as pd
from scipy.stats import truncnorm

# use a truncated normal distribution to generate a random
# skill rating between 0 and 100, for a given mean and std dev
def truncated_norm(mean, std_dev):
    a = (0 - mean) / std_dev
    b = (100 - mean) / std_dev
    return truncnorm.rvs(a, b, loc=mean, scale=std_dev)

class pg:
    def __init__(self):
        # attributes
        self.outside_scoring = truncated_norm(80,15)
        self.inside_scoring = truncated_norm(60,10)
        self.defending = truncated_norm(70,20)
        self.athleticism = truncated_norm(80,10)
        self.playmaking = truncated_norm(85,10)
        self.rebounding = truncated_norm(60,15)
        self.intangibles = truncated_norm(70,5)
        self.attributes = [self.outside_scoring, self.inside_scoring, self.defending, 
                self.athleticism, self.playmaking, self.rebounding, self.intangibles]
        # define overall to be the average of the top 3 attributes
        self.overall = np.mean(sorted(self.attributes)[-3:])

        # define expected values of a player's stats
        self.pts = 0.1 * (self.outside_scoring + self.inside_scoring)
        self.reb = 0.1 * self.rebounding
        self.ast = 0.07 * self.playmaking

class sg:
    def __init__(self):
        # attributes
        self.outside_scoring = truncated_norm(85,15)
        self.inside_scoring = truncated_norm(60,10)
        self.defending = truncated_norm(70,20)
        self.athleticism = truncated_norm(80,10)
        self.playmaking = truncated_norm(75,15)
        self.rebounding = truncated_norm(60,15)
        self.intangibles = truncated_norm(70,5)
        self.attributes = [self.outside_scoring, self.inside_scoring, self.defending, 
                self.athleticism, self.playmaking, self.rebounding, self.intangibles]
        # define overall to be the average of the top 3 attributes
        self.overall = np.mean(sorted(self.attributes)[-3:])

        # define expected values of a player's stats
        self.pts = 0.1 * (self.outside_scoring + self.inside_scoring)
        self.reb = 0.1 * self.rebounding
        self.ast = 0.07 * self.playmaking

class sf:
    def __init__(self):
        # attributes
        self.outside_scoring = truncated_norm(75,15)
        self.inside_scoring = truncated_norm(75,15)
        self.defending = truncated_norm(75,15)
        self.athleticism = truncated_norm(75,15)
        self.playmaking = truncated_norm(60,15)
        self.rebounding = truncated_norm(75,15)
        self.intangibles = truncated_norm(70,5)
        self.attributes = [self.outside_scoring, self.inside_scoring, self.defending, 
                self.athleticism, self.playmaking, self.rebounding, self.intangibles]
        # define overall to be the average of the top 3 attributes
        self.overall = np.mean(sorted(self.attributes)[-3:])

        # define expected values of a player's stats
        self.pts = 0.1 * (self.outside_scoring + self.inside_scoring)
        self.reb = 0.1 * self.rebounding
        self.ast = 0.07 * self.playmaking

class pf:
    def __init__(self):
        # attributes
        self.outside_scoring = truncated_norm(60,15)
        self.inside_scoring = truncated_norm(80,10)
        self.defending = truncated_norm(80,10)
        self.athleticism = truncated_norm(70,15)
        self.playmaking = truncated_norm(60,15)
        self.rebounding = truncated_norm(80,15)
        self.intangibles = truncated_norm(70,5)
        self.attributes = [self.outside_scoring, self.inside_scoring, self.defending, 
                self.athleticism, self.playmaking, self.rebounding, self.intangibles]
        # define overall to be the average of the top 3 attributes
        self.overall = np.mean(sorted(self.attributes)[-3:])

        # define expected values of a player's stats
        self.pts = 0.1 * (self.outside_scoring + self.inside_scoring)
        self.reb = 0.1 * self.rebounding
        self.ast = 0.07 * self.playmaking

class c:
    def __init__(self):
        # attributes
        self.outside_scoring = truncated_norm(50,15)
        self.inside_scoring = truncated_norm(85,15)
        self.defending = truncated_norm(80,15)
        self.athleticism = truncated_norm(60,10)
        self.playmaking = truncated_norm(60,15)
        self.rebounding = truncated_norm(85,5)
        self.intangibles = truncated_norm(70,5)
        self.attributes = [self.outside_scoring, self.inside_scoring, self.defending, 
                self.athleticism, self.playmaking, self.rebounding, self.intangibles]
        # define overall to be the average of the top 3 attributes
        self.overall = np.mean(sorted(self.attributes)[-3:])

        # define expected values of a player's stats
        self.pts = 0.1 * (self.outside_scoring + self.inside_scoring)
        self.reb = 0.1 * self.rebounding
        self.ast = 0.07 * self.playmaking

        
class team:
    def __init__(self):
        # roster
        self.pg = pg()
        self.sg = sg()
        self.sf = sf()
        self.pf = pf()
        self.c = c()
        # overall rating
        self.overall = np.mean([self.pg.overall, self.sg.overall, self.sf.overall, self.pf.overall, self.c.overall])

        # expected stats
        self.pts = self.pg.pts + self.sg.pts + self.sf.pts + self.pf.pts + self.c.pts
        self.reb = self.pg.reb + self.sg.reb + self.sf.reb + self.pf.reb + self.c.reb
        self.ast = self.pg.ast + self.sg.ast + self.sf.ast + self.pf.ast + self.c.ast