import pandas as pd
import numpy as np
import plotly.express as px

def read_and_process_data(file_path, position, filter_col, filter_value, percent_col, numerator, denominator):
    df = pd.read_csv(file_path)
    # remove rows with 0 attempts
    df = df[df[filter_col] != filter_value]
    # add column for FG% or FG3%
    df[percent_col] = df[numerator] / df[denominator]
    # exclude outliers of 0% and 100%
    df = df[df[percent_col].between(0.01, 0.99)]  
    # add column for position
    df['Position'] = position
    return df

# File paths and position labels
files_positions = [
    ('data/fg2_data_guards.csv', 'G'),
    ('data/fg2_data_forwards.csv', 'F'),
    ('data/fg2_data_centers.csv', 'C'),
    ('data/fg3_data_guards.csv', 'G'),
    ('data/fg3_data_forwards.csv', 'F'),
    ('data/fg3_data_centers.csv', 'C'),
]

# Process each file
dataframes = []
for file, position in files_positions:
    if 'fg3' in file:
        df = read_and_process_data(file, position, 'Total_FG3A', 0.0, 'FG3%', 'Total_FG3M', 'Total_FG3A')
    else:
        df = read_and_process_data(file, position, 'Total_FG2A', 0.0, 'FG2%', 'Total_FG2M', 'Total_FG2A')
    dataframes.append(df)

# Combine dataframes for FG% and FG3%
fg2_data = pd.concat(dataframes[:3])
fg3_data = pd.concat(dataframes[3:])

# Histograms
fg2_fig = px.histogram(fg2_data, x='FG2%', title='Two-point field goal percentage by NBA starters, 2003-2022', color='Position', marginal='rug', opacity=0.7, nbins=100, barmode='group')
fg3_fig = px.histogram(fg3_data, x='FG3%', title='Three-point field goal percentage by NBA starters, 2003-2022', color='Position', marginal='rug', opacity=0.7, nbins=100, barmode='group')

# save images
fg2_fig.write_image("images/fg2_fig.png")
fg3_fig.write_image("images/fg3_fig.png")
fg2_fig.write_html('html_files/fg2_fig.html', include_plotlyjs='cdn')
fg3_fig.write_html('html_files/fg3_fig.html', include_plotlyjs='cdn')

#fg_fig.show()
#fg3_fig.show()

# calculate mean and standard deviation for each position
mean_g, std_g = fg2_data[fg2_data['Position'] == 'G']['FG2%'].mean(), fg2_data[fg2_data['Position'] == 'G']['FG2%'].std()
mean_f, std_f = fg2_data[fg2_data['Position'] == 'F']['FG2%'].mean(), fg2_data[fg2_data['Position'] == 'F']['FG2%'].std()
mean_c, std_c = fg2_data[fg2_data['Position'] == 'C']['FG2%'].mean(), fg2_data[fg2_data['Position'] == 'C']['FG2%'].std()
# same for FG3%
mean_g3, std_g3 = fg3_data[fg3_data['Position'] == 'G']['FG3%'].mean(), fg3_data[fg3_data['Position'] == 'G']['FG3%'].std()
mean_f3, std_f3 = fg3_data[fg3_data['Position'] == 'F']['FG3%'].mean(), fg3_data[fg3_data['Position'] == 'F']['FG3%'].std()
mean_c3, std_c3 = fg3_data[fg3_data['Position'] == 'C']['FG3%'].mean(), fg3_data[fg3_data['Position'] == 'C']['FG3%'].std()

# print the means and stds
print('FG%')
print('G: mean = {:.2f}, std = {:.2f}'.format(mean_g, std_g))
print('F: mean = {:.2f}, std = {:.2f}'.format(mean_f, std_f))
print('C: mean = {:.2f}, std = {:.2f}'.format(mean_c, std_c))
print('FG3%')
print('G: mean = {:.2f}, std = {:.2f}'.format(mean_g3, std_g3))
print('F: mean = {:.2f}, std = {:.2f}'.format(mean_f3, std_f3))
print('C: mean = {:.2f}, std = {:.2f}'.format(mean_c3, std_c3))


# now look at rebounds and assists

starter_stats = pd.read_csv('data/starter_stats.csv')

fig_reb = px.histogram(starter_stats, x='REB', 
                   color='START_POSITION',  # Column to group by
                   nbins=50,  # Number of bins
                   title='Rebounds in a game by NBA starters, 2003-2022',
                   labels={'REB': 'Rebounds', 'START_POSITION': 'Position'},  # Rename axis
                   barmode='group') 

fig_ast = px.histogram(starter_stats, x='AST', 
                   color='START_POSITION',  # Column to group by
                   nbins=50,  # Number of bins
                   title='Assists in a game by NBA starters, 2003-2022',
                   labels={'AST': 'Assists', 'START_POSITION': 'Position'},  # Rename axis
                   barmode='group')  


fig_reb.write_image("images/fig_reb_by_pos.png")
fig_ast.write_image("images/fig_ast_by_pos.png")
fig_reb.write_html('html_files/fig_reb.html', include_plotlyjs='cdn')
fig_ast.write_html('html_files/fig_ast.html', include_plotlyjs='cdn')