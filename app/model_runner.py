import random
from datetime import datetime
from app.config import settings

def load_model():
    # Placeholder: Simulate loading model
    return "dummy_model"

def predict(stock_data: dict):
    """
    Simulates prediction.

    stock_data = {
        "AAPL": {"price": 211.11, "volume": 1000, "time": "..."},
        "MSFT": {"price": 500.55, "volume": 800, "time": "..."}
    }

    Returns:
    {
        "AAPL": {"predicted": 212.03, "time": "..."},
        "MSFT": {"predicted": 499.87, "time": "..."}
    }
    """
    prediction = {}
    for symbol, data in stock_data.items():
        actual_price = data["price"]
        predicted_price = actual_price + random.uniform(-1.5, 1.5)  # Random noise
        prediction[symbol] = {
            "predicted": round(predicted_price, 2),
            "time": datetime.utcnow().isoformat()
        }
    return prediction
