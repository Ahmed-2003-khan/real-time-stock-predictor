import asyncio
import yfinance as yf
import pandas as pd
from datetime import datetime
from app.config import settings
from app.model_runner import predict
import os

RAW_DATA_PATH = "data/raw_data.csv"
OHLC_DATA_PATH = "data/ohlc_data.csv"
AGG_INTERVAL_MINUTES = 15

def aggregate_to_ohlc():
    if not os.path.exists(RAW_DATA_PATH):
        return

    df = pd.read_csv(RAW_DATA_PATH, parse_dates=["time"])

    # Round timestamps down to nearest aggregation window
    df["rounded_time"] = df["time"].dt.floor(f"{AGG_INTERVAL_MINUTES}min")

    ohlc = (
        df.groupby(["symbol", "rounded_time"])
        .agg(open=("price", "first"),
             high=("price", "max"),
             low=("price", "min"),
             close=("price", "last"),
             volume=("volume", "sum"))
        .reset_index()
        .rename(columns={"rounded_time": "time"})
    )

    if not ohlc.empty:
        header_needed = not os.path.exists(OHLC_DATA_PATH)
        ohlc.to_csv(OHLC_DATA_PATH, mode="a", header=header_needed, index=False)

async def fetch_loop():
    counter = 0
    print("🔄 fetch_loop started...")  # ✅ Add this
    while True:
        print("📡 Fetching data...")   # ✅ Add this
        data = {}
        for symbol in settings.symbols:
            ticker = yf.Ticker(symbol)
            try:
                info = ticker.info
                data[symbol] = {
                    "price": info.get("currentPrice"),
                    "volume": info.get("volume"),
                    "time": datetime.utcnow().isoformat()
                }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")

        if data:
            df = pd.DataFrame([
                {
                    "symbol": sym,
                    "price": val["price"],
                    "volume": val["volume"],
                    "time": val["time"]
                }
                for sym, val in data.items()
            ])
            df["time"] = pd.to_datetime(df["time"])
            df.to_csv(RAW_DATA_PATH, mode="a", header=not os.path.exists(RAW_DATA_PATH), index=False)
            print("Fetched:", data)

        counter += 1
        # Aggregate every 15 mins worth of data
        if counter * settings.fetch_interval >= AGG_INTERVAL_MINUTES * 60:
            print("🔁 Aggregating to OHLC")
            aggregate_to_ohlc()
            counter = 0

            # ✅ Auto-trigger forecast after aggregation
            print("🔮 Auto-forecast triggered...")
            predict()

        await asyncio.sleep(settings.fetch_interval)
