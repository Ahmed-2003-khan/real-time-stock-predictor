import asyncio
import csv
import os
from app.fetch_data import fetch_latest_prices
from app.config import settings

DATA_FILE = "data/stock_data.csv"

async def fetch_loop():
    while True:
        prices = fetch_latest_prices()
        print("Fetched:", prices)

        # Save to CSV
        file_exists = os.path.isfile(DATA_FILE)
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["symbol", "price", "volume", "time"])
            for symbol, info in prices.items():
                writer.writerow([symbol, info["price"], info["volume"], info["time"]])
        
        await asyncio.sleep(settings.fetch_interval)
