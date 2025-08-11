import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Database connection string
db_user = "user"
db_password = "password"
db_host = "localhost"
db_port = "5432"
db_name = "bootcamp_db"
db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create engine
engine = create_engine(db_url)

# CSV paths - dictionary
csv_files = {
    "customers": "datasets/customers.csv",
    "accounts": "datasets/accounts.csv",
    "transactions": "datasets/transactions.csv",
    # "time": "datasets/time.csv"
}

# Load and insert
for table, path in csv_files.items():
    df = pd.read_csv(path)
    print(f"Inserting {len(df)} records into {table}...")
    df.to_sql(table, engine, if_exists='append', index=False)
    print(f"{table} inserted successfully.")

print("All tables inserted into PostgreSQL.")