import os
import sqlite3
import pandas as pd

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
    cursor.execute("PRAGMA table_info(data_table)")
    columns = cursor.fetchall()
    conn.close()
    return {
        "table_name": "data_table",
        "columns": [{"name": col[1], "type": col[2]} for col in columns]
    }
