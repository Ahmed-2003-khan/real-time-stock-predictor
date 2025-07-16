from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    symbols: List[str] = ["AAPL"]
    fetch_interval: int = 900  # 15 minutes
    retrain_threshold: float = 0.1

    class Config:
        env_file = ".env"
        case_sensitive = False

    @classmethod
    def customise_sources(cls, init_settings, env_settings, file_secret_settings):
        from pydantic import Field
        from pydantic_settings.sources import EnvSettingsSource

        # Parse CSV string to list
        class CustomEnvSource(EnvSettingsSource):
            def get_field_value(self, field: Field, field_name: str):
                value, source = super().get_field_value(field, field_name)
                if field_name == "symbols" and isinstance(value, str):
                    value = [s.strip() for s in value.split(",")]
                return value, source

        return (
            init_settings,
            CustomEnvSource,
            file_secret_settings,
        )
