import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
from datetime import datetime

def calculate_metrics(csv_path: str, window_size: int = 10):
    try:
        df = pd.read_csv(csv_path)

        # Keep only the last N predictions for evaluation
        df = df.sort_values(by="time").groupby("symbol").tail(window_size)

        y_true = df["actual"]
        y_pred = df["predicted"]

        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

        return {
            "RMSE": round(rmse, 4),
            "MAE": round(mae, 4),
            "MAPE": round(mape, 2)
        }

    except Exception as e:
        return {"error": str(e)}

def save_metrics(metrics: dict, path: str = "logs/metrics.csv"):
    """
    Appends evaluated metrics to CSV with a timestamp.
    """
    metrics["time"] = datetime.utcnow().isoformat()
    df = pd.DataFrame([metrics])
    df.to_csv(path, mode="a", header=not os.path.exists(path), index=False)