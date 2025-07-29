import asyncio
import yfinance as yf
import pandas as pd
from datetime import datetime
from app.config import settings
from app.model_runner import predict
import os

RAW_DATA_PATH = "data/raw_data.csv"

async def fetch_loop():
    print("🔄 fetch_loop started...")

    while True:
        print("📡 Fetching latest price...")
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
                print(f"❌ Error fetching {symbol}: {e}")

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
            print("✅ Saved raw data:", data)

            # 🔮 Trigger forecast immediately
            print("🔮 Making prediction...")
            predict()

        await asyncio.sleep(settings.fetch_interval)

if __name__ == "__main__":
    asyncio.run(fetch_loop())
