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
    ('data/fg3_data_centers.csv', 'C')
]

# Process each file
dataframes = []
for file, position in files_positions:
    if 'fg3' in file:
        df = read_and_process_data(file, position, 'Total_FG3A', 0.0, 'FG3%', 'Total_FG3M', 'Total_FG3A')
    else:
        df = read_and_process_data(file, position, 'Total_FG2A', 0.0, 'FG%', 'Total_FG2M', 'Total_FG2A')
    dataframes.append(df)

# Combine dataframes for FG% and FG3%
fg2_data = pd.concat(dataframes[:3])
fg3_data = pd.concat(dataframes[3:])

# Histograms
fg2_fig = px.histogram(fg2_data, x='FG%', color='Position', marginal='rug', opacity=0.7, nbins=100, barmode='group')
fg3_fig = px.histogram(fg3_data, x='FG3%', color='Position', marginal='rug', opacity=0.7, nbins=100, barmode='group')

# save images
fg2_fig.write_image("images/fg_fig.png")
fg3_fig.write_image("images/fg3_fig.png")

#fg_fig.show()
#fg3_fig.show()

# calculate mean and standard deviation for each position
mean_g, std_g = fg2_data[fg2_data['Position'] == 'G']['FG%'].mean(), fg2_data[fg2_data['Position'] == 'G']['FG%'].std()
mean_f, std_f = fg2_data[fg2_data['Position'] == 'F']['FG%'].mean(), fg2_data[fg2_data['Position'] == 'F']['FG%'].std()
mean_c, std_c = fg2_data[fg2_data['Position'] == 'C']['FG%'].mean(), fg2_data[fg2_data['Position'] == 'C']['FG%'].std()
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
