from datetime import datetime, timedelta
import pandas as pd
import os
from app.model_utils import load_forecast_model, forecast_next_n_prices
from app.config import settings

PRED_PATH = "logs/predictions.csv"
OHLC_PATH = "data/ohlc_data.csv"

def predict(n_steps=10):
    if not os.path.exists(OHLC_PATH):
        return {}

    df = pd.read_csv(OHLC_PATH, parse_dates=["time"])

    # Focus on AAPL only (as agreed)
    symbol = "AAPL"
    df_symbol = df[df["symbol"] == symbol].sort_values(by="time")

    if len(df_symbol) < 30:
        print("⚠️ Not enough data to make forecast")
        return {"message": "Not enough data to forecast."}

    # Get last 30 close prices
    recent_closes = df_symbol["price"].values[-30:]

    try:
        model, scaler = load_forecast_model()
        predictions = forecast_next_n_prices(model, scaler, recent_closes, n_steps=n_steps)

        now = datetime.utcnow()
        forecast_data = []

        for i, pred in enumerate(predictions):
            forecast_time = now + timedelta(minutes=(i + 1) * settings.aggregation_minutes)
            forecast_data.append({
                "symbol": symbol,
                "time": forecast_time.isoformat(),
                "predicted": round(float(pred), 2),
                "actual": None
            })

        # Save to CSV
        df_forecast = pd.DataFrame(forecast_data)
        df_forecast.to_csv(PRED_PATH, mode="a", header=not os.path.exists(PRED_PATH), index=False)

        return {symbol: forecast_data}

    except Exception as e:
        return {"error": str(e)}
