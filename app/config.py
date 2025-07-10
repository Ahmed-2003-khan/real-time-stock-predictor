from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    symbols: List[str]
    fetch_interval: int
    retrain_threshold: float

    class Config:
        env_file = ".env"

settings = Settings()
