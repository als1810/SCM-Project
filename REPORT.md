# Project Report: Supply Chain Management Dashboard (P1: Order & Inventory Visibility)

## 1. Problem Statement Analysis

### Scope
This project addresses P1: Order & Inventory Visibility, focusing on difficulties in tracking orders, shipments, delays, bottlenecks, and inventory levels in e-commerce supply chains.

### SCM Areas Addressed
- Order tracking and monitoring
- Shipment visibility and delay identification
- Inventory management and low-stock alerts
- Demand forecasting for optimized inventory

### Proposed Solution
An interactive Streamlit dashboard with real-time KPIs, visualizations, and ML-based predictions to enable data-driven decisions.

### Business Impact
Reduces delays, prevents stockouts, improves efficiency, and enhances customer satisfaction.

## 2. Dashboard Design & Development

### Features
- **Overview**: KPIs (total orders, delivery rates), order trends chart.
- **Inventory**: Stock levels bar chart, low-stock alerts table.
- **Shipments**: Status pie chart, delay histogram.
- **Predictions**: Demand forecast line chart with Linear Regression and ARIMA.

### KPIs Included
- Total Orders
- On-Time Delivery Rate
- Delayed Orders Percentage
- Average Delivery Time
- Inventory Levels (via charts)
- Low Stock Alerts

### Interactivity
- Sidebar navigation
- Date range and product filters
- Drill-down via charts

## 3. Data Structure and Sample Data

### Database Schema
- **Orders**: order_id, product_id, customer_id, order_date, delivery_date, status, quantity
- **Shipments**: shipment_id, order_id, warehouse_id, dispatch_date, delivery_date, status, delay_days
- **Inventory**: product_id, warehouse_id, stock_level, reorder_level, last_updated
- **Products**: product_id, product_name, category, price
- **Warehouses**: warehouse_id, location, capacity

### Sample Data Generation
- Synthetic data for 1000 orders over 6 months
- Includes delays, inventory fluctuations
- Stored in SQLite database via Python scripts

## 4. Machine Learning Integration

### Models Used
- **Linear Regression**: Predicts demand based on historical trends.
- **ARIMA**: Time series model for seasonal forecasting.

### Training and Validation
- Trained on daily order quantities
- Evaluated with MSE (Linear Regression: ~X, ARIMA: ~Y, based on data)
- Predictions for next 30 days saved to CSV

### Benefits
- Optimizes inventory by forecasting demand
- Prevents overstocking/understocking
- Enhances decision-making with predictive insights

## 5. Documentation and Presentation

### Methodology
- Data generation → Database setup → ML training → Dashboard development
- Tools: Python, Pandas, SQLite, Streamlit, Plotly, Scikit-learn, Statsmodels

### Assumptions
- Synthetic data mimics real scenarios
- Models assume linear/seasonal patterns; real data may vary

### Insights Derived
- Identification of delay patterns (e.g., avg delay X days)
- Low-stock risks for products Y
- Demand peaks in certain periods
- Improved visibility leads to X% efficiency gains (estimated)

### Challenges and Learnings
- Data quality affects ML accuracy
- Balancing simplicity with realism
- Learned dashboard interactivity and ML integration

## 6. Final Presentation & Demonstration

### Structure (10 minutes)
- Intro: Problem and solution (2 min)
- Demo: Dashboard walkthrough with filters (5 min)
- ML Explanation: Models and predictions (2 min)
- Insights and Future Work (1 min)

### Tools for Presentation
- Live demo in browser
- Screenshots for backup

## References
- ThoughtSpot: Supply Chain KPIs
- Project Templates: KPI Dashboards
- Commport: Top SCM Metrics

## Author
Akshaj L Shastry

## Submission Details
File: SCM22CS_P1_001-002-003.pdf (adjust SRNs)
Upload to Google Drive by 20/04/2026