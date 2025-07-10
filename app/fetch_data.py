import yfinance as yf
import pandas as pd
from datetime import datetime
from app.config import settings

def fetch_latest_prices():
    symbols = settings.symbols
    data = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d", interval="1m")  # 1-day, 1-minute interval
        if not hist.empty:
            latest = hist.iloc[-1]
            data[symbol] = {
                "price": float(latest["Close"]),
                "volume": float(latest["Volume"]),
                "time": datetime.now().isoformat()
            }
    return data
