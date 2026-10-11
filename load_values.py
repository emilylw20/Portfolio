import pandas as pd
import sqlite3
from config import  DB_NAME

# Load 50-row CSV file
df = pd.read_csv("stores.csv")

# Dump it into SQLite
conn = sqlite3.connect(DB_NAME)
df.to_sql("retail_stores", conn, if_exists="replace", index=False)
cursor = conn.cursor()

print("Database created and seeded successfully!")

# Create table to hold event data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_outbox (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        store_id INTEGER,
        payload TEXT,
        status TEXT DEFAULT 'PENDING'
    )
''')
conn.close()

