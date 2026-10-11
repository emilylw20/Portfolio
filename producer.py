import json
import math
import sqlite3
import json 
from config import DB_NAME

class Customer:
    def __init__ (self, location):
        self.location = location
        self.orders = []

class Product:
    def __init__ (self,product_id ):
        self.product_id = product_id
        self.is_stocked = True

class RetailStore:
    def __init__ (self, store_id, location, total_products, is_stocked):
        self.total_products = total_products
        self.store_id = store_id
        self.location = location 
        self.is_stocked = is_stocked
        self.distribution_center_stocked = True

class WarehouseManager:
    def __init__ (self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.list_of_stores = []

    def load_stores_from_sql(self):
        self.list_of_stores = []
        self.cursor.execute("SELECT store_id, x_coord, y_coord, total_products, is_stocked FROM retail_stores")
        rows = self.cursor.fetchall()
        for row in rows:
            store = RetailStore(store_id=row[0], location = (row[1], row[2]), total_products= row[3], is_stocked = bool(row[4]))
            self.list_of_stores.append(store)
    
    def route_location(self, customer):
        self.load_stores_from_sql()
        best_store_id = None
        smallest_distance = float('inf')
        for store in self.list_of_stores: 
            if not store.is_stocked:
                continue
            distance = math.sqrt((customer.location[0] - store.location[0])**2 + (customer.location[1] - store.location[1])**2) # calculate distance 
            if distance < smallest_distance:
                smallest_distance = distance
                best_store_id = store.store_id
        if best_store_id is None:
            return "No stocked Stores found"
        event_data = {
            "event": "ORDER_ROUTED_EVENT",
            "store_id": best_store_id
        }
        self.cursor.execute(
            "INSERT INTO event_outbox (event_type, store_id, payload, status) VALUES (?, ?, ?, ?)",
            ("ORDER_ROUTED", best_store_id, json.dumps(event_data), "PENDING")
        )
        self.conn.commit()

       
        return f"Fulfillment Verified: Roted to store {best_store_id}"

customer_order = Customer((120, 230))
manager = WarehouseManager()
print(manager.route_location(customer_order))