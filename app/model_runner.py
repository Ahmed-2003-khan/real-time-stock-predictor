import random
from datetime import datetime, timezone
from app.config import settings
import csv

def load_model():
    # Placeholder: Simulate loading model
    return "dummy_model"

def predict(stock_data: dict):
    """
    Simulates prediction.

    stock_data = {
        "AAPL": {"price": 211.11, "volume": 1000, "time": "..."},
        "MSFT": {"price": 500.55, "volume": 800, "time": "..."}
    }

    Returns:
    {
        "AAPL": {"predicted": 212.03, "time": "..."},
        "MSFT": {"predicted": 499.87, "time": "..."}
    }
    """
    prediction = {}
    now = datetime.now(timezone.utc).isoformat()

    with open("data/predictions.csv", "a", newline="") as f:
        writer = csv.writer(f)

        for symbol, data in stock_data.items():
            actual_price = data["price"]
            predicted_price = actual_price + random.uniform(-1.5, 1.5)

            prediction[symbol] = {
                "predicted": round(predicted_price, 2),
                "time": now
            }

            # Log: symbol, prediction time, actual, predicted
            writer.writerow([symbol, now, actual_price, round(predicted_price, 2)])

    return prediction
