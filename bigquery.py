import bigquery

# create Client object
client = bigquery.client()

# construct reference to dataset: csv file 'game_stats.csv'
dataset_ref = client.dataset('game_stats')