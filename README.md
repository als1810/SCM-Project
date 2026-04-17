# 📦 Supply Chain Management Dashboard (P1: Order & Inventory Visibility)

## 📌 Project Overview

This project is developed as part of the **UE23CS342BA1 – Supply Chain Management for Engineers** course.

The goal of this project is to design and implement an **interactive dashboard** that provides real-time visibility into **orders, shipments, and inventory** within an e-commerce supply chain.

The system enables decision-makers to:

* Track order and shipment status
* Identify delays and bottlenecks
* Monitor inventory levels
* Predict future demand using machine learning

---

## 🎯 Problem Statement (P1 – Order & Inventory Visibility)

Organizations often face challenges in:

* Tracking orders and shipments in real-time
* Identifying delays and bottlenecks
* Managing inventory efficiently

This project provides a **centralized dashboard solution** to address these issues using data visualization and predictive analytics.

---

## 🧠 Objectives

* Provide real-time visibility into supply chain operations
* Enable data-driven decision making
* Detect delays and inventory issues
* Forecast future demand using ML models

---

## 🏗️ System Architecture

```
CSV Data Generation → SQLite Database → Python Processing → ML Models → Streamlit Dashboard
```

---

## 🛠️ Tech Stack

### Backend / Data Processing

* Python (Pandas, NumPy)

### Database

* SQLite

### Dashboard

* Streamlit
* Plotly (for interactive visualizations)

### Machine Learning

* Scikit-learn / Statsmodels

---

## 🗄️ Database Schema

### Tables:

1. **Orders**

   * order_id
   * product_id
   * customer_id
   * order_date
   * delivery_date
   * status
   * quantity

2. **Shipments**

   * shipment_id
   * order_id
   * warehouse_id
   * dispatch_date
   * delivery_date
   * status
   * delay_days

3. **Inventory**

   * product_id
   * warehouse_id
   * stock_level
   * reorder_level
   * last_updated

4. **Products**

   * product_id
   * product_name
   * category
   * price

5. **Warehouses**

   * warehouse_id
   * location
   * capacity

---

## 📊 Key Performance Indicators (KPIs)

The dashboard tracks important supply chain KPIs such as:

* Total Orders
* On-Time Delivery Rate
* Delayed Orders Percentage
* Average Delivery Time
* Inventory Levels
* Low Stock Alerts

These KPIs help monitor efficiency and identify bottlenecks in the supply chain ([ThoughtSpot][1])

---

## 📁 Dataset

* Synthetic dataset generated using Python
* Mimics real-world supply chain operations
* Includes:

  * Order history (last 6 months)
  * Shipment delays
  * Inventory fluctuations

---

## 🤖 Machine Learning

### Demand Forecasting

* Model: Linear Regression / Time Series (ARIMA)
* Input: Historical order data
* Output: Future demand predictions

### Use Case:

* Helps optimize inventory levels
* Prevents stockouts and overstocking

---

## 🖥️ Dashboard Features

### 📌 Overview

* KPI cards
* Order trends over time

### 📦 Inventory

* Stock levels per product
* Low stock alerts

### 🚚 Shipments

* Shipment status breakdown
* Delayed shipments analysis

### 🤖 Predictions

* Future demand visualization

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone <repo-url>
cd scm-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Dataset

```bash
python data/generate_data.py
```

### 4. Run Application

```bash
streamlit run dashboard/app.py
```

---

## 📊 Project Structure

```
scm-dashboard/
│
├── data/
│   ├── generate_data.py
│   ├── orders.csv
│   ├── shipments.csv
│   ├── inventory.csv
│
├── database/
│   ├── db_setup.py
│   ├── scm.db
│
├── ml/
│   ├── forecasting.py
│
├── dashboard/
│   ├── app.py
│
├── requirements.txt
└── README.md
```

---

## 📈 Insights (Expected)

* Identification of delayed shipment patterns
* Detection of low inventory risks
* Forecast-driven inventory planning
* Improved decision-making efficiency

---

## 🚀 Future Enhancements

* Real-time data integration
* Advanced ML models (LSTM, Prophet)
* Supplier performance tracking
* API-based architecture

---

## 👨‍💻 Author

* Akshaj L Shastry

---

## 📚 References

* Supply Chain KPI dashboards help monitor performance and enable data-driven decisions across logistics and inventory systems ([Project Templates][2])
* Common KPIs include inventory turnover, on-time delivery, and order fulfillment metrics ([Commport Communications][3])

---

[1]: https://www.thoughtspot.com/data-trends/dashboard/supply-chain-kpis-metrics-for-dashboard?utm_source=chatgpt.com "15 supply chain KPIs and metrics you should track in 2024"
[2]: https://www.projectmanagertemplate.com/post/supply-chain-kpi-dashboard?utm_source=chatgpt.com "Supply Chain KPI Dashboard - Project Management Templates"
[3]: https://www.commport.com/top-30-supply-chain-metrics-and-kpis-you-should-be-monitoring/?utm_source=chatgpt.com "Top 30 Supply Chain KPIs to Track | Download the Full List ..."