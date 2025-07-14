import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

MODEL_PATH = "models/lstm_forecast_model.h5"
SCALER_PATH = "models/scaler.save"

def load_forecast_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError("Model or scaler file not found.")
    
    model = load_model(MODEL_PATH, compile=False)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

def prepare_input_sequence(series: np.ndarray, window_size: int = 30):
    """
    Convert last window_size values into model input shape: (1, window_size, 1)
    """
    return series[-window_size:].reshape(1, window_size, 1)

def forecast_next_n_prices(model, scaler, close_prices: list, n_steps: int = 10):
    """
    Generate N-step forecast using last closing prices
    """
    scaled_series = scaler.transform(np.array(close_prices).reshape(-1, 1))
    window_size = len(close_prices)
    
    input_seq = scaled_series[-window_size:].reshape(1, window_size, 1)
    
    predictions = model.predict(input_seq, verbose=0)[0]  # shape (10,)
    forecasts = scaler.inverse_transform(predictions.reshape(-1, 1)).flatten()
    return forecasts
