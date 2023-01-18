from typing import Optional
from enum import Enum, auto
from pydantic import BaseSettings, validator
from pathlib import Path

class Settings(BaseSettings):
    database_type: str
    deployment: Optional[str] = ""
    database_name: Optional[str] = None
    database_password: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    class Config:
        env_file = f"{Path(__file__).resolve().parent}/.env"

    @validator('database_type')
    def determine_correct_database_type(cls, value: str):
        storage_mapping = {"SQLITE": StorageType.SQLITE,
                           "POSTGRES": StorageType.POSTGRES,
                           "DUMMY_DATA": StorageType.DUMMY_DATA,
                           "FAKE_DB": StorageType.FAKE_DB}
        if value.upper() not in storage_mapping.keys():
            raise ValueError(f'Incorrect database type provided: {value}. '
                             f'Use one of the following: {list(storage_mapping.keys())}')
        return storage_mapping[value.upper()]

    @validator('deployment')
    def check_deployment_type(cls, value: str):
        deployment_mapping = {"PRODUCTION": DeploymentType.PRODUCTION,
                              "LOCAL": DeploymentType.LOCAl,
                              "": ""}
        if value.upper() not in deployment_mapping.keys():
            raise ValueError(f'Incorrect deployment type provided: {value}. '
                             f'Use one of the following: {list(deployment_mapping.keys())}')
        return deployment_mapping[value.upper()]

    # TODO: add a validator that checks that if deployment type is production that aws secrets are available


class StorageType(Enum):
    SQLITE = auto()
    POSTGRES = auto()
    DUMMY_DATA = auto()
    FAKE_DB = auto()


class DeploymentType(Enum):
    PRODUCTION = auto()
    LOCAl = auto()


SETTINGS = Settings()
