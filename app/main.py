from fastapi import FastAPI
from app.config import settings
from app.scheduler import fetch_loop
from app.model_runner import predict
import asyncio
import pandas as pd
from app.evaluator import calculate_metrics
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
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
        df = pd.read_csv("data/data.csv")
        latest_data = df.groupby("symbol").tail(1)

        stock_input = {
            row["symbol"]: {
                "price": row["price"],
                "volume": row["volume"],
                "time": row["time"]
            }
            for _, row in latest_data.iterrows()
        }

        result = predict(stock_input)
        return result

    except Exception as e:
        return {"error": str(e)}
    
@app.get("/metrics")
def get_metrics():
    result = calculate_metrics("logs/predictions.csv", window_size=10)
    return result

