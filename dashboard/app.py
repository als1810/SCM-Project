import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime

# Load data
conn = sqlite3.connect('database/scm.db')
orders_df = pd.read_sql_query("SELECT * FROM Orders", conn)
shipments_df = pd.read_sql_query("SELECT * FROM Shipments", conn)
inventory_df = pd.read_sql_query("SELECT * FROM Inventory", conn)
products_df = pd.read_sql_query("SELECT * FROM Products", conn)
warehouses_df = pd.read_sql_query("SELECT * FROM Warehouses", conn)
conn.close()

# Load predictions
predictions_df = pd.read_csv('ml/predictions.csv')

# Dashboard
st.title("📦 Supply Chain Management Dashboard")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Inventory", "Shipments", "Predictions"])

# Filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", [pd.to_datetime(orders_df['order_date']).min(), pd.to_datetime(orders_df['order_date']).max()])
selected_products = st.sidebar.multiselect("Select Products", products_df['product_name'].unique(), default=products_df['product_name'].unique())
selected_warehouses = st.sidebar.multiselect("Select Warehouses", warehouses_df['location'].unique(), default=warehouses_df['location'].unique())

# Filter data
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
filtered_orders = orders_df[(orders_df['order_date'] >= pd.to_datetime(date_range[0])) & (orders_df['order_date'] <= pd.to_datetime(date_range[1]))]
filtered_orders = filtered_orders[filtered_orders['product_id'].isin(products_df[products_df['product_name'].isin(selected_products)]['product_id'])]

warehouse_ids = warehouses_df[warehouses_df['location'].isin(selected_warehouses)]['warehouse_id']
filtered_shipments = shipments_df[shipments_df['warehouse_id'].isin(warehouse_ids)]
filtered_shipments = filtered_shipments[filtered_shipments['order_id'].isin(filtered_orders['order_id'])]

filtered_inventory = inventory_df[inventory_df['warehouse_id'].isin(warehouse_ids)]
filtered_inventory = filtered_inventory[filtered_inventory['product_id'].isin(products_df[products_df['product_name'].isin(selected_products)]['product_id'])]

if page == "Overview":
    st.header("📌 Overview")
    
    # KPIs
    total_orders = len(filtered_orders)
    on_time_delivery = len(filtered_orders[filtered_orders['status'] == 'Delivered']) / total_orders * 100 if total_orders > 0 else 0
    delayed_orders = len(filtered_shipments[filtered_shipments['delay_days'] > 0]) / len(filtered_shipments) * 100 if len(filtered_shipments) > 0 else 0
    avg_delivery_time = filtered_shipments['delay_days'].mean() if len(filtered_shipments) > 0 else 0
    fill_rate = len(filtered_orders[filtered_orders['status'].isin(['Delivered', 'Shipped'])]) / total_orders * 100 if total_orders > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Orders", total_orders)
    col2.metric("On-Time Delivery Rate", f"{on_time_delivery:.2f}%", delta=f"{on_time_delivery - 75:.1f}%", delta_color="normal" if on_time_delivery >= 70 else "inverse")
    col3.metric("Delayed Orders %", f"{delayed_orders:.2f}%", delta=f"{delayed_orders - 10:.1f}%", delta_color="inverse" if delayed_orders > 15 else "normal")
    col4.metric("Avg Delivery Time (days)", f"{avg_delivery_time:.2f}", delta=f"{avg_delivery_time - 2:.1f}", delta_color="inverse" if avg_delivery_time > 2 else "normal")
    col5.metric("Fill Rate", f"{fill_rate:.2f}%", delta=f"{fill_rate - 90:.1f}%", delta_color="normal" if fill_rate >= 85 else "inverse")
    
    # Order trends
    order_trends = filtered_orders.groupby('order_date')['quantity'].sum().reset_index()
    fig = px.line(order_trends, x='order_date', y='quantity', title='Order Trends Over Time')
    st.plotly_chart(fig)
    
    # Insights
    st.subheader("Insights")
    st.write("""
    - On-time delivery is stable at ~76%, but delays still exist in certain shipments.
    - Order trends show seasonal demand peaks; monitor inventory accordingly.
    - Overall efficiency supports data-driven decisions for supply chain optimization.
    """)

elif page == "Inventory":
    st.header("📦 Inventory")
    
    # Stock levels
    inventory_merged = pd.merge(filtered_inventory, products_df, on='product_id')
    inventory_merged = pd.merge(inventory_merged, warehouses_df, on='warehouse_id')
    fig = px.bar(inventory_merged, x='product_name', y='stock_level', color='location', title='Stock Levels per Product')
    st.plotly_chart(fig)
    
    # Low stock alerts
    low_stock = inventory_merged[inventory_merged['stock_level'] < inventory_merged['reorder_level']]
    st.subheader("Low Stock Alerts")
    st.dataframe(low_stock[['product_name', 'location', 'stock_level', 'reorder_level']])
    
    # Insights
    st.info("Low stock items require immediate replenishment to avoid stockouts. Review reorder levels for high-demand products.")

elif page == "Shipments":
    st.header("🚚 Shipments")
    
    # Shipment status
    status_counts = filtered_shipments['status'].value_counts()
    fig = px.pie(status_counts, names=status_counts.index, title='Shipment Status Breakdown')
    st.plotly_chart(fig)
    
    # Delayed shipments
    delayed = filtered_shipments[filtered_shipments['delay_days'] > 0]
    fig2 = px.histogram(delayed, x='delay_days', title='Delayed Shipments Analysis')
    st.plotly_chart(fig2)
    
    # Delayed shipments table
    st.subheader("Delayed Shipments Details")
    st.dataframe(delayed[['shipment_id', 'order_id', 'warehouse_id', 'delay_days']])
    
    # Avg delay per warehouse
    avg_delay_warehouse = filtered_shipments.groupby('warehouse_id')['delay_days'].mean().reset_index()
    avg_delay_warehouse = pd.merge(avg_delay_warehouse, warehouses_df, on='warehouse_id')
    st.subheader("Average Delay per Warehouse")
    st.dataframe(avg_delay_warehouse[['location', 'delay_days']])
    
    # Trend over time
    filtered_shipments['dispatch_date'] = pd.to_datetime(filtered_shipments['dispatch_date'])
    delay_trend = filtered_shipments.groupby('dispatch_date')['delay_days'].mean().reset_index()
    fig3 = px.line(delay_trend, x='dispatch_date', y='delay_days', title='Delay Trend Over Time')
    st.plotly_chart(fig3)
    
    # Insights
    st.info("Focus on warehouses with high average delays for process improvement. Delays indicate supply chain bottlenecks.")

elif page == "Predictions":
    st.header("🤖 Predictions")
    
    # Future demand
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=predictions_df['date'], y=predictions_df['linear_regression'], mode='lines', name='Linear Regression'))
    fig.add_trace(go.Scatter(x=predictions_df['date'], y=predictions_df['arima'], mode='lines', name='ARIMA'))
    fig.update_layout(title='Future Demand Predictions', xaxis_title='Date', yaxis_title='Predicted Quantity')
    st.plotly_chart(fig)
    
    # Model Explanation
    st.subheader("Model Explanation")
    st.write("**Linear Regression** uses historical order quantity trends to forecast demand.")
    st.write("**ARIMA** forecasts demand as a time series model that captures trend and seasonality.")
    st.write("These forecasts help improve inventory planning and reduce stockouts.")
    
    # Business insight
    st.info("Demand is expected to remain stable over the next 30 days.")
    st.warning("Consider increasing stock for high-demand products to avoid shortages.")

st.sidebar.info("Dashboard for P1: Order & Inventory Visibility")