import os
import sqlite3
import pandas as pd
from typing import List, Dict

def build_sqlite_table_from_csv(csv_path: str, sqlite_path: str = "data/data.sqlite") -> None:
    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(sqlite_path)
    df.to_sql("data_table", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()


def extract_sqlite_schema(sqlite_path: str) -> dict:
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    
    # Get basic column info
    cursor.execute("PRAGMA table_info(data_table)")
    columns = cursor.fetchall()
    
    # Get sample values for each column
    column_data = []
    for col in columns:
        col_name = col[1]
        # Get 3 distinct sample values, excluding NULL/empty values
        cursor.execute(f"""
            SELECT DISTINCT "{col_name}" 
            FROM data_table 
            WHERE "{col_name}" IS NOT NULL AND "{col_name}" != ''
            LIMIT 5
        """)
        sample_values = [str(row[0]) for row in cursor.fetchall()]
        
        column_data.append({
            "name": col_name,
            "type": col[2],
            "sample_values": sample_values
        })
    
    conn.close()
    return {
        "table_name": "data_table",
        "columns": column_data
    }
