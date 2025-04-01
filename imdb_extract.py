import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os

# Remote IMDb SQL connection
MYSQL_URL = "mysql+pymysql://guest:ctu-relational@relational.fel.cvut.cz:3306/imdb_ijs"
sqlite_path = "data/imdb_full.sqlite"

# Tables to copy
tables = ["actors", "movies", "directors", "directors_genres", "movies_directors", "movies_genres", "roles"]

# Delete existing file if it exists
if os.path.exists(sqlite_path):
    os.remove(sqlite_path)
    print(f"🗑️ Removed existing SQLite DB at {sqlite_path}")

# Create engines
mysql_engine = create_engine(MYSQL_URL)
sqlite_conn = sqlite3.connect(sqlite_path)

# Full data pull
for table in tables:
    print(f"📥 Copying {table}...")
    df = pd.read_sql(f"SELECT * FROM {table}", con=mysql_engine)
    df.to_sql(table, sqlite_conn, index=False, if_exists="replace")
    print(f"✅ {table} → {len(df)} rows")

sqlite_conn.close()
print(f"\n Done! Full IMDb subset stored in {sqlite_path}")
