from fastapi import FastAPI
from app.config import settings
from app.scheduler import fetch_loop
from app.model_runner import predict
import asyncio
import pandas as pd
from app.evaluator import calculate_metrics
from contextlib import asynccontextmanager
import os



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logi
    task = asyncio.create_task(fetch_loop())
    yield
    # Shutdown logic (optional)
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}

@app.get("/config")
def get_config():
    return {
        "symbols": settings.symbols,
        "interval": settings.fetch_interval,
        "threshold": settings.retrain_threshold
    }

@app.get("/predict")
def make_prediction():
    try:
        result = predict()
        return result

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/metrics")
def get_metrics():
    result = calculate_metrics("logs/predictions.csv", window_size=10)
    return result


@app.get("/metrics/history")
def get_metrics_history():
    try:
        df = pd.read_csv("logs/metrics.csv")
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/forecast")
def get_latest_forecast():
    pred_path = "logs/predictions.csv"

    if not os.path.exists(pred_path):
        return {"message": "No forecast data available yet."}

    try:
        df = pd.read_csv(pred_path)

        # Keep only latest 20 rows
        latest = df.sort_values(by="time", ascending=False).head(20)

        result = []
        for _, row in latest.iterrows():
            result.append({
                "symbol": row["symbol"],
                "time": row["time"],
                "predicted": float(row["predicted"]) if pd.notna(row["predicted"]) else None,
                "actual": float(row["actual"]) if pd.notna(row.get("actual", None)) else None
            })

        return {"forecasts": result}

    except Exception as e:
        return {"error": str(e)}




