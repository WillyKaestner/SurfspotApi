from src.config import SETTINGS, StorageType
from src.database import session
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
        repository = crud_location.SqlAlchemyLocation(db=session.get_db(), is_sqlite=True)
        return repository
    if SETTINGS.database_type == StorageType.POSTGRES:
        repository = crud_location.SqlAlchemyLocation(db=session.get_db(), is_sqlite=False)
        return repository
    if SETTINGS.database_type == StorageType.DUMMY_DATA:
        repository = crud_location.DummyLocation()
        return repository
