import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('database/scm.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Warehouses (
    warehouse_id INTEGER PRIMARY KEY,
    location TEXT,
    capacity INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    delivery_date DATE,
    status TEXT,
    quantity INTEGER,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Shipments (
    shipment_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    warehouse_id INTEGER,
    dispatch_date DATE,
    delivery_date DATE,
    status TEXT,
    delay_days INTEGER,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Inventory (
    product_id INTEGER,
    warehouse_id INTEGER,
    stock_level INTEGER,
    reorder_level INTEGER,
    last_updated DATE,
    PRIMARY KEY (product_id, warehouse_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
)
''')

# Load data from CSV and insert
products_df = pd.read_csv('data/products.csv')
products_df.to_sql('Products', conn, if_exists='replace', index=False)

warehouses_df = pd.read_csv('data/warehouses.csv')
warehouses_df.to_sql('Warehouses', conn, if_exists='replace', index=False)

orders_df = pd.read_csv('data/orders.csv')
orders_df.to_sql('Orders', conn, if_exists='replace', index=False)

shipments_df = pd.read_csv('data/shipments.csv')
shipments_df.to_sql('Shipments', conn, if_exists='replace', index=False)

inventory_df = pd.read_csv('data/inventory.csv')
inventory_df.to_sql('Inventory', conn, if_exists='replace', index=False)

conn.commit()
conn.close()

print("Database setup complete.")