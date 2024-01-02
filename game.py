import numpy as np
from rosters import team

class game:
    def __init__(self, team1, team2, game_number, stats, team_stats):
        np.random.seed(None)
    
        self.game_number = game_number
        self.team1 = team1
        self.team2 = team2
        self.stats = stats
        self.team_stats = team_stats
        self.positions = ['pg', 'sg', 'sf', 'pf', 'c']

        # Calculate penalties for each position
        self.penalties = {pos: (getattr(team1, pos).overall - getattr(team2, pos).overall) / 100. 
                          for pos in self.positions}
        
        # Calculate box scores for both teams
        self.team1_box = self.calculate_box_score(team1, 1)
        self.team2_box = self.calculate_box_score(team2, -1)

    # Function to calculate box score for a team, and store the stats for each player
    def calculate_box_score(self, team, penalty_multiplier):
        box_scores = []
        for pos in self.positions:
            player = getattr(team, pos)
            penalty = self.penalties[pos] * penalty_multiplier
            # pick a random number from a Poisson distribution with mean = player.pts * (1 + penalty), etc.
            pts = np.ceil(np.random.poisson(player.pts * (1 + penalty)))
            reb = np.ceil(np.random.poisson(player.reb * (1 + penalty)))
            ast = np.ceil(np.random.poisson(player.ast * (1 + penalty)))
            box_scores.append([pts, reb, ast])
            self.stats[team.seed, self.game_number, np.where(np.array(self.positions) == pos)[0][0], :] = [pts, reb, ast]
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

    # Keep track of W-L record for each team
    def win_loss(self):
        team1_pts = np.sum(self.team1_box[:, 0])
        team2_pts = np.sum(self.team2_box[:, 0])
        if team1_pts > team2_pts:
            self.team_stats[self.team1.seed, 0] += 1
            self.team_stats[self.team2.seed, 1] += 1
        elif team2_pts > team1_pts:
            self.team_stats[self.team1.seed, 1] += 1
            self.team_stats[self.team2.seed, 0] += 1
        else:
            self.team_stats[self.team1.seed, 2] += 1
            self.team_stats[self.team2.seed, 2] += 1