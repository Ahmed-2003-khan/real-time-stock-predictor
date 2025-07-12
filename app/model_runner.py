import random
from datetime import datetime
from app.config import settings
import pandas as pd
import os
from app.evaluator import calculate_metrics, save_metrics


def load_model():
    # Placeholder for real model loading later
    return "dummy_model"


def predict(stock_data: dict):
    """
    Simulates predictions and saves them with timestamps.
    Also evaluates performance and saves metrics.
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

    # Save predictions to CSV
    pred_path = "logs/predictions.csv"
    df = pd.DataFrame(rows)
    df.to_csv(pred_path, mode="a", header=not os.path.exists(pred_path), index=False)

    # Evaluate metrics and save
    metrics = calculate_metrics(pred_path, window_size=10)
    save_metrics(metrics)

    return {
        "prediction": prediction,
        "metrics": metrics
    }
