import src.database as db
from src.config import SETTINGS, StorageType
from src.crud import crud_location

def get_crud_location() -> crud_location.AbstractLocation:
    """
    Factory function that creates the crud logic for receiving location data based on the selected storage type.

    - SQLITE: SQLAlchemy ORM to work with SQLite databases
    - POSTGRES: SQLAlchemy ORM to work with Postgres databases
    - DUMMY_DATA: Sample data

    Returns:
        Repository instance based on the selected storage type
    """
    if SETTINGS.database_type == StorageType.SQLITE:
        repository = crud_location.SqlAlchemyLocation(db=db.get_db(), is_sqlite=True)
        return repository
    if SETTINGS.database_type == StorageType.POSTGRES or SETTINGS.database_type == StorageType.LIGHTSAIL_POSTGRES:
        repository = crud_location.SqlAlchemyLocation(db=db.get_db(), is_sqlite=False)
        return repository
    if SETTINGS.database_type == StorageType.DUMMY_DATA:
        repository = crud_location.DummyLocation()
        return repository
    if SETTINGS.database_type == StorageType.FAKE_DB:
        repository = crud_location.FakeDB()
        return repository
