import pandas as pd
import os
from sqlalchemy import create_engine

# credentials
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
dbname = os.getenv('DB_NAME')
db_type = 'mysql+pymysql'

# database connection
conn_str = f'{db_type}://{user}:{password}@{host}:{port}/{dbname}'

# create an engine
engine = create_engine(conn_str, echo=False)

# query
query = 'SELECT game_id FROM game_stats WHERE pos_id = 0 AND stat_id = 0 AND value > 20.0'

# Execute the query and store the results in a pandas DataFrame
with engine.connect() as connection:
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

print(df)