import json
import sqlite3
from config import DB_NAME


print("Local Event Consumer is listening...")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("SELECT event_id, payload FROM event_outbox WHERE status = 'PENDING'  ")
events = cursor.fetchall()

for event_id, raw_payload in events:
    event_data = json.loads(raw_payload)
    if event_data is None:
        continue

    print(f"\n [Event Recieved]: {event_data['event']}")
    store_id = event_data['store_id']
    cursor.execute("UPDATE retail_stores SET total_products = total_products -1 WHERE store_id = ?", (store_id,))
    cursor.execute("UPDATE event_outbox SET status = 'PROCESSED' WHERE event_id = ?", (event_id,))
    conn.commit()

    print(f"[STATE SYNC] Inventory decremented for Store ID {store_id} & Event Marked Processed")
