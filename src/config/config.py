from enum import Enum, auto
from pydantic import BaseSettings, validator
from pathlib import Path

class Settings(BaseSettings):
    database_type: str
    database_name: str
    database_password: str = ""

    class Config:
        env_file = f"{Path(__file__).resolve().parent}/.env"

    @validator('database_type')
    def name_must_contain_space(cls, value: str):
        storage_mapping = {"SQLITE": StorageType.SQLITE,
                           "POSTGRES": StorageType.POSTGRES,
                           "DUMMY_DATA": StorageType.DUMMY_DATA,
                           "FAKE_DB": StorageType.FAKE_DB}
        if value.upper() not in storage_mapping.keys():
            raise ValueError(f'Incorrect database type provided: {value}. '
                             f'Use one of the following: {list(storage_mapping.keys())}')
        return storage_mapping[value.upper()]


class StorageType(Enum):
    SQLITE = auto()
    POSTGRES = auto()
    DUMMY_DATA = auto()
    FAKE_DB = auto()


SETTINGS = Settings()

