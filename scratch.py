import pandas as pd

# import data from starter_stats.csv
starter_stats = pd.read_csv('data/starter_stats.csv', index_col=0)

stats = ['OREB', 'DREB', 'STL', 'BLK', 'TO', 'AST']
positions = ['G', 'F', 'C']

# calculate the mean of each of stats for START_POSITION = all of the positions in positions
for position in positions:
    for stat in stats:
        print(stat, position, starter_stats.loc[starter_stats['START_POSITION'] == position, stat].mean())