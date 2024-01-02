import pandas as pd
import plotly.express as px

# read in data from nba_data/starter_stats.csv
starter_stats = pd.read_csv('nba_data/starter_stats.csv')

fig_pts = px.histogram(starter_stats, x='PTS', 
                   color='START_POSITION',  # Column to group by
                   nbins=50,  # Number of bins
                   title='Points scored in a game by NBA starters',
                   labels={'PTS': 'Points', 'START_POSITION': 'Position'},  # Rename axis
                   barmode='group')  # Color of the histogram

fig_reb = px.histogram(starter_stats, x='REB', 
                   color='START_POSITION',  # Column to group by
                   nbins=50,  # Number of bins
                   title='Rebounds in a game by NBA starters',
                   labels={'REB': 'Rebounds', 'START_POSITION': 'Position'},  # Rename axis
                   barmode='group')  # Color of the histogram

fig_ast = px.histogram(starter_stats, x='AST', 
                   color='START_POSITION',  # Column to group by
                   nbins=50,  # Number of bins
                   title='Assists in a game by NBA starters',
                   labels={'AST': 'Assists', 'START_POSITION': 'Position'},  # Rename axis
                   barmode='group')  # Color of the histogram

fig_pts.update_layout(bargap=0.1)  # Gap between bars
fig_reb.update_layout(bargap=0.1)  # Gap between bars
fig_ast.update_layout(bargap=0.1)  # Gap between bars
#fig_pts.show()

fig_pts.write_image("images/fig_pts_by_pos.png")
fig_reb.write_image("images/fig_reb_by_pos.png")
fig_ast.write_image("images/fig_ast_by_pos.png")