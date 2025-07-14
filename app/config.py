from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    symbols: List[str]
    fetch_interval: int
    retrain_threshold: float
    aggregation_minutes: int = 15


    class Config:
        env_file = ".env"

settings = Settings()
