import asyncio
from fastapi import FastAPI
from app.config import settings
from app.scheduler import fetch_loop
from app.model_runner import predict
import asyncio
import pandas as pd
from app.evaluator import calculate_metrics
from contextlib import asynccontextmanager
import os
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logi
    task = asyncio.create_task(fetch_loop())
    yield
    # Shutdown logic (optional)
    task.cancel()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        latest = df.sort_values(by="time", ascending=True).head(10)

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
    
@app.get("/actuals")
def get_actuals():
    path = "data/raw_data.csv"

    if not os.path.exists(path):
        return {"message": "No actual data yet."}

    try:
        df = pd.read_csv(path)
        df = df[df["symbol"] == "AAPL"].sort_values(by="time", ascending=False).head(25)
        df = df.sort_values(by="time")

        result = []
        for _, row in df.iterrows():
            result.append({
                "time": row["time"],
                "actual": float(row["price"])
            })

        return {"actuals": result}

    except Exception as e:
        return {"error": str(e)}



@app.on_event("startup")
async def start_scheduler():
    asyncio.create_task(fetch_loop())

