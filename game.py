import numpy as np
from rosters import truncated_norm, team

class game:
    def __init__(self, team1, team2):
        np.random.seed(None)
        
        self.team1 = team1
        self.team2 = team2
        self.positions = ['pg', 'sg', 'sf', 'pf', 'c']

        # Calculate penalties for each position
        self.penalties = {pos: (getattr(team1, pos).overall - getattr(team2, pos).overall) / 100. 
                          for pos in self.positions}
        
        # Calculate box scores for both teams
        self.team1_box = self.calculate_box_score(team1, 1)
        self.team2_box = self.calculate_box_score(team2, -1)

    def calculate_box_score(self, team, penalty_multiplier):
        box_scores = []
        for pos in self.positions:
            player = getattr(team, pos)
            penalty = self.penalties[pos] * penalty_multiplier
            pts = np.ceil(truncated_norm(player.pts * (1 + penalty), 5))
            reb = np.ceil(truncated_norm(player.reb * (1 + penalty), 5))
            ast = np.ceil(truncated_norm(player.ast * (1 + penalty), 5))
            box_scores.append([pts, reb, ast])
        return np.array(box_scores)

    # Display box score for a team
    def display_box(self, team_box, team):
        print(team.name)
        for i, pos in enumerate(self.positions):
            print(f"{pos.upper()}: {team_box[i, 0]} pts, {team_box[i, 1]} reb, {team_box[i, 2]} ast")
        print()

    # Display box scores for both teams
    def box_score(self):
        self.display_box(self.team1_box, self.team1)
        self.display_box(self.team2_box, self.team2)

    # Display final score
    def result(self):
        team1_pts = np.sum(self.team1_box[:, 0])
        team2_pts = np.sum(self.team2_box[:, 0])
        print(f'{self.team1.name}: {team1_pts} points')
        print(f'{self.team2.name}: {team2_pts} points')

        
eagles = team(name="Eagles",seed=1)
falcons = team(name="Falcons",seed=2)

game1 = game(eagles, falcons)
game1.box_score()
game1.result()
