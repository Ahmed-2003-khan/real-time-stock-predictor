import random
from datetime import datetime
from app.config import settings
import pandas as pd
import os

def load_model():
    # Placeholder model
    return "dummy_model"

def predict(stock_data: dict):
    """
    Simulates predictions and saves them with timestamps.
    """
    prediction = {}
    rows = []

    for symbol, data in stock_data.items():
        actual_price = data["price"]
        predicted_price = actual_price + random.uniform(-1.5, 1.5)
        prediction[symbol] = {
            "predicted": round(predicted_price, 2),
            "actual": round(actual_price, 2),
            "time": datetime.utcnow().isoformat()
        }

        rows.append({
            "symbol": symbol,
            "predicted": round(predicted_price, 2),
            "actual": round(actual_price, 2),
            "time": datetime.utcnow().isoformat()
        })

    # Save to CSV
    pred_path = "logs/predictions.csv"
    df = pd.DataFrame(rows)
    df.to_csv(pred_path, mode="a", header=not os.path.exists(pred_path), index=False)

    return prediction
