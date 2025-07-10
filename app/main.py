from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.scheduler import fetch_loop
from app.config import settings
import asyncio

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
