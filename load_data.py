import pandas as pd
from sqlalchemy import create_engine
print("Starting the data loading process for the Fact Table...")

# Read only the third file (the one that got stuck in workbench)
print("Reading 'fact_ev_registrations.csv' into memory...")
fact_ev_registrations = pd.read_csv("fact_ev_registrations.csv")

# Database connection Credentials
user = 'root'
password = '707933'
host = 'localhost'
database = 'ev_analytics_db'

# Create a connection engine using SQLAlchemy
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# Puse only the third file directly into the mysql database
print("pusing 285,000+ rows to mysql... Plese wait... 10-15 seaconds.")

# Note on if_exists='replace': If the previous manual import created a partial/broken table,
# This will safely drop it and create freash, clean table.
fact_ev_registrations.to_sql('fact_ev_registrations', con=engine, if_exists='replace', index=False, chunksize=10000)

print("\nSuccess! The Fact Table has been successfully loaded.")
print("your ETL pipeline is row complete, and all data is ready in MySQL!")
