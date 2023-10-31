import numpy as np
from rosters import truncated_norm, team

class game:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

        # matchup penalties: if a player's overall rating is lower than the opposing player's,
        # reduce their expected stats by that percentage
        self.pg_penalty = (team1.pg.overall - team2.pg.overall) / 100.
        self.sg_penalty = (team1.sg.overall - team2.sg.overall) / 100.
        self.sf_penalty = (team1.sf.overall - team2.sf.overall) / 100.
        self.pf_penalty = (team1.pf.overall - team2.pf.overall) / 100.
        self.c_penalty = (team1.c.overall - team2.c.overall) / 100.

        self.team1_pg = np.ceil(np.array([truncated_norm(team1.pg.pts * (1+self.pg_penalty) , 5), 
                          truncated_norm(team1.pg.reb * (1+self.pg_penalty) , 5),
                          truncated_norm(team1.pg.ast * (1+self.pg_penalty) , 5)]))
        self.team1_sg = np.ceil(np.array([truncated_norm(team1.sg.pts * (1+self.sg_penalty) , 5),
                            truncated_norm(team1.sg.reb * (1+self.sg_penalty) , 5),
                            truncated_norm(team1.sg.ast * (1+self.sg_penalty) , 5)]))
        self.team1_sf = np.ceil(np.array([truncated_norm(team1.sf.pts * (1+self.sf_penalty) , 5),
                            truncated_norm(team1.sf.reb * (1+self.sf_penalty) , 5),
                            truncated_norm(team1.sf.ast * (1+self.sf_penalty) , 5)]))
        self.team1_pf = np.ceil(np.array([truncated_norm(team1.pf.pts * (1+self.pf_penalty) , 5),
                            truncated_norm(team1.pf.reb * (1+self.pf_penalty) , 5),
                            truncated_norm(team1.pf.ast * (1+self.pf_penalty) , 5)]))
        self.team1_c = np.ceil(np.array([truncated_norm(team1.c.pts * (1+self.c_penalty) , 5),
                            truncated_norm(team1.c.reb * (1+self.c_penalty) , 5),
                            truncated_norm(team1.c.ast * (1+self.c_penalty) , 5)]))
        
        self.team2_pg = np.ceil(np.array([truncated_norm(team2.pg.pts * (1-self.pg_penalty) , 5),
                            truncated_norm(team2.pg.reb * (1-self.pg_penalty) , 5),
                            truncated_norm(team2.pg.ast * (1-self.pg_penalty) , 5)]))
        self.team2_sg = np.ceil(np.array([truncated_norm(team2.sg.pts * (1-self.sg_penalty) , 5),
                            truncated_norm(team2.sg.reb * (1-self.sg_penalty) , 5),
                            truncated_norm(team2.sg.ast * (1-self.sg_penalty) , 5)]))
        self.team2_sf = np.ceil(np.array([truncated_norm(team2.sf.pts * (1-self.sf_penalty) , 5),
                            truncated_norm(team2.sf.reb * (1-self.sf_penalty) , 5),
                            truncated_norm(team2.sf.ast * (1-self.sf_penalty) , 5)]))
        self.team2_pf = np.ceil(np.array([truncated_norm(team2.pf.pts * (1-self.pf_penalty) , 5),
                            truncated_norm(team2.pf.reb * (1-self.pf_penalty) , 5),
                            truncated_norm(team2.pf.ast * (1-self.pf_penalty) , 5)]))
        self.team2_c = np.ceil(np.array([truncated_norm(team2.c.pts * (1-self.c_penalty) , 5),
                            truncated_norm(team2.c.reb * (1-self.c_penalty) , 5),
                            truncated_norm(team2.c.ast * (1-self.c_penalty) , 5)]))

        self.team1_box = np.vstack((self.team1_pg, self.team1_sg, self.team1_sf, self.team1_pf, self.team1_c))
        self.team2_box = np.vstack((self.team2_pg, self.team2_sg, self.team2_sf, self.team2_pf, self.team2_c))
        
    def box_score(self):
        print('Team 1')
        print('PG: {} pts, {} reb, {} ast'.format(self.team1_box[0,0], self.team1_box[0,1], self.team1_box[0,2]))
        print('SG: {} pts, {} reb, {} ast'.format(self.team1_box[1,0], self.team1_box[1,1], self.team1_box[1,2]))
        print('SF: {} pts, {} reb, {} ast'.format(self.team1_box[2,0], self.team1_box[2,1], self.team1_box[2,2]))
        print('PF: {} pts, {} reb, {} ast'.format(self.team1_box[3,0], self.team1_box[3,1], self.team1_box[3,2]))
        print('C: {} pts, {} reb, {} ast'.format(self.team1_box[4,0], self.team1_box[4,1], self.team1_box[4,2]))

        print('Team 2')
        print('PG: {} pts, {} reb, {} ast'.format(self.team2_box[0,0], self.team2_box[0,1], self.team2_box[0,2]))
        print('SG: {} pts, {} reb, {} ast'.format(self.team2_box[1,0], self.team2_box[1,1], self.team2_box[1,2]))
        print('SF: {} pts, {} reb, {} ast'.format(self.team2_box[2,0], self.team2_box[2,1], self.team2_box[2,2]))
        print('PF: {} pts, {} reb, {} ast'.format(self.team2_box[3,0], self.team2_box[3,1], self.team2_box[3,2]))
        print('C: {} pts, {} reb, {} ast'.format(self.team2_box[4,0], self.team2_box[4,1], self.team2_box[4,2]))

    def result(self):
        team1_pts = np.sum(self.team1_box[1:,0])
        team2_pts = np.sum(self.team2_box[1:,0])
        print('Team 1: {} points'.format(team1_pts))
        print('Team 2: {} points'.format(team2_pts))
        
team1 = team()
team2 = team()

game1 = game(team1, team2)
game1.box_score()
game1.result()
