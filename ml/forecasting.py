import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import sqlite3

# Load data
conn = sqlite3.connect('database/scm.db')
orders_df = pd.read_sql_query("SELECT * FROM Orders", conn)
conn.close()

# Prepare data for forecasting
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
orders_df = orders_df.sort_values('order_date')
daily_orders = orders_df.groupby('order_date')['quantity'].sum().reset_index()

# Linear Regression for demand forecasting
X = np.arange(len(daily_orders)).reshape(-1, 1)
y = daily_orders['quantity'].values
model = LinearRegression()
model.fit(X, y)

# Predict next 30 days
future_days = np.arange(len(daily_orders), len(daily_orders) + 30).reshape(-1, 1)
predictions_lr = model.predict(future_days)

# Evaluate Linear Regression (using last 10 days as test)
if len(daily_orders) > 10:
    X_train = X[:-10]
    y_train = y[:-10]
    X_test = X[-10:]
    y_test = y[-10:]
    model_eval = LinearRegression()
    model_eval.fit(X_train, y_train)
    y_pred = model_eval.predict(X_test)
    mse_lr = mean_squared_error(y_test, y_pred)
    print(f"Linear Regression MSE: {mse_lr:.2f}")
else:
    mse_lr = None

# ARIMA for time series forecasting
arima_model = ARIMA(daily_orders['quantity'], order=(5,1,0))
arima_fit = arima_model.fit()
predictions_arima = arima_fit.forecast(steps=30)

# Evaluate ARIMA
if len(daily_orders) > 10:
    train = daily_orders['quantity'][:-10]
    test = daily_orders['quantity'][-10:]
    arima_eval = ARIMA(train, order=(5,1,0))
    arima_eval_fit = arima_eval.fit()
    arima_pred = arima_eval_fit.forecast(steps=10)
    mse_arima = mean_squared_error(test, arima_pred)
    print(f"ARIMA MSE: {mse_arima:.2f}")
else:
    mse_arima = None

# Save predictions
predictions_df = pd.DataFrame({
    'date': pd.date_range(start=daily_orders['order_date'].max() + pd.Timedelta(days=1), periods=30),
    'linear_regression': predictions_lr,
    'arima': predictions_arima
})
predictions_df.to_csv('ml/predictions.csv', index=False)

print("Forecasting complete. Models evaluated.")