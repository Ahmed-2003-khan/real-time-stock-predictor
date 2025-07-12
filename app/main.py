from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.scheduler import fetch_loop
from app.config import settings
import asyncio
from app.model_runner import predict
import pandas as pd
from app.evaluator import compute_metrics



@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👇 Start background task
    task = asyncio.create_task(fetch_loop())
    
    yield  # 👈 Control passes to the app here

    # (Optional) Cancel background task on shutdown
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
        df = pd.read_csv("data/stock_data.csv")  # Load recent data
        latest_data = df.groupby("symbol").tail(1)  # Get last row per stock

        stock_input = {
            row["symbol"]: {
                "price": row["price"],
                "volume": row["volume"],
                "time": row["time"]
            }
            for _, row in latest_data.iterrows()
        }

        result = predict(stock_input)  # Call fake model
        return result
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/metrics")
def get_metrics():
    return compute_metrics()
