import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate data for the last 6 months
start_date = datetime.now() - timedelta(days=180)
end_date = datetime.now()

# Products
products = [
    {'product_id': 1, 'product_name': 'Laptop', 'category': 'Electronics', 'price': 1000},
    {'product_id': 2, 'product_name': 'Mouse', 'category': 'Electronics', 'price': 20},
    {'product_id': 3, 'product_name': 'Keyboard', 'category': 'Electronics', 'price': 50},
    {'product_id': 4, 'product_name': 'Monitor', 'category': 'Electronics', 'price': 200},
    {'product_id': 5, 'product_name': 'Chair', 'category': 'Furniture', 'price': 150},
    {'product_id': 6, 'product_name': 'Desk', 'category': 'Furniture', 'price': 300},
    {'product_id': 7, 'product_name': 'Book', 'category': 'Stationery', 'price': 10},
    {'product_id': 8, 'product_name': 'Pen', 'category': 'Stationery', 'price': 2},
]

products_df = pd.DataFrame(products)
products_df.to_csv('data/products.csv', index=False)

# Warehouses
warehouses = [
    {'warehouse_id': 1, 'location': 'New York', 'capacity': 10000},
    {'warehouse_id': 2, 'location': 'Los Angeles', 'capacity': 8000},
    {'warehouse_id': 3, 'location': 'Chicago', 'capacity': 6000},
]

warehouses_df = pd.DataFrame(warehouses)
warehouses_df.to_csv('data/warehouses.csv', index=False)

# Generate Orders
orders = []
order_id = 1
statuses = ['Delivered'] * 80 + ['Shipped'] * 10 + ['Pending'] * 5 + ['Cancelled'] * 5  # Weighted for realism
for _ in range(1000):  # 1000 orders
    order_date = start_date + timedelta(days=random.randint(0, 180))
    delivery_date = order_date + timedelta(days=random.randint(1, 14))
    status = random.choice(statuses)
    if status == 'Delivered':
        delivery_date = order_date + timedelta(days=random.randint(1, 10))
    elif status == 'Shipped':
        delivery_date = order_date + timedelta(days=random.randint(1, 5))
    else:
        delivery_date = pd.NaT
    orders.append({
        'order_id': order_id,
        'product_id': random.choice(products)['product_id'],
        'customer_id': random.randint(1, 500),
        'order_date': order_date.date(),
        'delivery_date': delivery_date.date() if pd.notna(delivery_date) else None,
        'status': status,
        'quantity': random.randint(1, 10)
    })
    order_id += 1

orders_df = pd.DataFrame(orders)
orders_df.to_csv('data/orders.csv', index=False)

# Generate Shipments
shipments = []
shipment_id = 1
for order in orders:
    if order['status'] in ['Shipped', 'Delivered']:
        dispatch_date = pd.to_datetime(order['order_date']) + timedelta(days=random.randint(0, 3))
        delay_prob = random.random()
        if delay_prob < 0.1:  # 10% chance of delay
            delay_days = random.randint(1, 5)
        else:
            delay_days = 0
        delivery_date = dispatch_date + timedelta(days=random.randint(1, 7) + delay_days)
        status = 'Delivered' if order['status'] == 'Delivered' else 'In Transit'
        shipments.append({
            'shipment_id': shipment_id,
            'order_id': order['order_id'],
            'warehouse_id': random.choice(warehouses)['warehouse_id'],
            'dispatch_date': dispatch_date.date(),
            'delivery_date': delivery_date.date(),
            'status': status,
            'delay_days': delay_days
        })
        shipment_id += 1

shipments_df = pd.DataFrame(shipments)
shipments_df.to_csv('data/shipments.csv', index=False)

# Generate Inventory
inventory = []
for product in products:
    for warehouse in warehouses:
        stock_level = random.randint(0, 1000)
        reorder_level = 100
        last_updated = datetime.now().date()
        inventory.append({
            'product_id': product['product_id'],
            'warehouse_id': warehouse['warehouse_id'],
            'stock_level': stock_level,
            'reorder_level': reorder_level,
            'last_updated': last_updated
        })

inventory_df = pd.DataFrame(inventory)
inventory_df.to_csv('data/inventory.csv', index=False)

print("Data generation complete.")