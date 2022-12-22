from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_type: str
    database_name: str
    database_password: str = ""

    class Config:
        env_file = f"{Path(__file__).resolve().parent}/.env"


settings = Settings()
