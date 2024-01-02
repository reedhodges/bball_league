import pandas as pd
import plotly.express as px

# read in data from nba_data/starter_stats.csv
starter_stats = pd.read_csv('nba_data/starter_stats.csv')

fig_pts = px.histogram(starter_stats, x='PTS', 
                   color='START_POSITION',  # Column to group by
                   nbins=50,  # Number of bins
                   title='Points scored in a game by NBA starters',
                   labels={'PTS': 'Points', 'START_POSITION': 'Position'},  # Rename axis
                   barmode='group')  

fig_reb = px.histogram(starter_stats, x='REB', 
                   color='START_POSITION',  # Column to group by
                   nbins=50,  # Number of bins
                   title='Rebounds in a game by NBA starters',
                   labels={'REB': 'Rebounds', 'START_POSITION': 'Position'},  # Rename axis
                   barmode='group') 

fig_ast = px.histogram(starter_stats, x='AST', 
                   color='START_POSITION',  # Column to group by
                   nbins=50,  # Number of bins
                   title='Assists in a game by NBA starters',
                   labels={'AST': 'Assists', 'START_POSITION': 'Position'},  # Rename axis
                   barmode='group')  

fig_pts.update_layout(bargap=0.1)  # Gap between bars
fig_reb.update_layout(bargap=0.1)  # Gap between bars
fig_ast.update_layout(bargap=0.1)  # Gap between bars
#fig_pts.show()

fig_pts.write_image("images/fig_pts_by_pos.png")
fig_reb.write_image("images/fig_reb_by_pos.png")
fig_ast.write_image("images/fig_ast_by_pos.png")

# create new df for each position
g_df = starter_stats[starter_stats['START_POSITION'] == 'G']
f_df = starter_stats[starter_stats['START_POSITION'] == 'F']
c_df = starter_stats[starter_stats['START_POSITION'] == 'C']

# estimate mean for each position and stat
g_pts_mean = g_df['PTS'].mean()
f_pts_mean = f_df['PTS'].mean()
c_pts_mean = c_df['PTS'].mean()
g_reb_mean = g_df['REB'].mean()
f_reb_mean = f_df['REB'].mean()
c_reb_mean = c_df['REB'].mean()
g_ast_mean = g_df['AST'].mean()
f_ast_mean = f_df['AST'].mean()
c_ast_mean = c_df['AST'].mean()

print('G mean points: ', g_pts_mean)
print('F mean points: ', f_pts_mean)
print('C mean points: ', c_pts_mean)
print('G mean rebounds: ', g_reb_mean)
print('F mean rebounds: ', f_reb_mean)
print('C mean rebounds: ', c_reb_mean)
print('G mean assists: ', g_ast_mean)
print('F mean assists: ', f_ast_mean)
print('C mean assists: ', c_ast_mean)



