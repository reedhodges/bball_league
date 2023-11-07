import pandas as pd
import os
from sqlalchemy import create_engine

# credentials
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
dbname = os.getenv('DB_NAME')
db_type='mysql+pymysql'

# database connection
conn_str = f'{db_type}://{user}:{password}@{host}:{port}/{dbname}'

# create an engine
engine = create_engine(conn_str, echo=False)

# load the dataset from csv
df = pd.read_csv('game_stats.csv')

# new column names
new_col_names = ['team_id', 'game_id', 'pos_id', 'stat_id', 'value']
# rename columns
df.columns = new_col_names

# write the data to the database
df.to_sql('game_stats', con=engine, index=False, if_exists='append')