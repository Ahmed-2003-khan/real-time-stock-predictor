import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

def compute_metrics():
    try:
        df = pd.read_csv("data/predictions.csv")
        if len(df) < 10:
            return {"note": "Not enough data yet to evaluate."}

        latest = df.groupby("symbol").tail(20)
        actual = latest["actual"]
        predicted = latest["predicted"]

        mae = mean_absolute_error(actual, predicted)
        rmse = mean_squared_error(actual, predicted, squared=False)
        mape = (abs((actual - predicted) / actual)).mean() * 100

        return {
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "MAPE (%)": round(mape, 2),
            "Samples": len(latest)
        }
    except Exception as e:
        return {"error": str(e)}
