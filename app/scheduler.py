import asyncio
import yfinance as yf
import pandas as pd
from datetime import datetime
from app.config import settings

async def fetch_loop():
    while True:
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
            df.to_csv("data/data.csv", mode="a", header=not pd.io.common.file_exists("data/data.csv"), index=False)
            print("Fetched:", data)
        
        await asyncio.sleep(settings.fetch_interval)
