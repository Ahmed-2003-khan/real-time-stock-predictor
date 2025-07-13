import random
from datetime import datetime, timedelta
from app.config import settings
import pandas as pd
import os
from app.evaluator import calculate_metrics, save_metrics

# Dummy model for simulation
def load_model():
    return "dummy_forecast_model"

def predict(stock_data: dict, steps: int = 10, interval: int = 60):
    """
    Simulate N-step forecasting for each stock symbol.
    steps: how many future points to predict
    interval: seconds between each step (default: 1 min = 60s)
    """
    forecast = {}
    rows = []

    now = datetime.utcnow()

    for symbol, data in stock_data.items():
        base_price = data["price"]
        symbol_forecast = []

        for step in range(steps):
            forecast_time = now + timedelta(seconds=(step + 1) * interval)
            predicted_price = base_price + random.uniform(-2.0, 2.0)
            symbol_forecast.append({
                "time": forecast_time.isoformat(),
                "predicted": round(predicted_price, 2),
                "actual": None,
                "symbol": symbol
            })

            rows.append({
                "symbol": symbol,
                "time": forecast_time.isoformat(),
                "predicted": round(predicted_price, 2),
                "actual": None
            })

        forecast[symbol] = symbol_forecast

    # Save to CSV
    pred_path = "logs/predictions.csv"
    df = pd.DataFrame(rows)

    # If file doesn't exist, write with header. Else, append without header
    write_header = not os.path.exists(pred_path)
    df.to_csv(pred_path, mode="a", header=write_header, index=False)

    return forecast
