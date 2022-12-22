from enum import Enum, auto
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.crud import crud_location
from src.config import settings

class InvalidStorageType(Exception):
    """Raised when the .env file provided an invalid database type"""


class StorageSource(Enum):
    SQLITE = auto()
    POSTGRES = auto()
    DUMMY_DATA = auto()


def read_storage_type(option: str) -> StorageSource:
    """
    Returns the correct enum object based on the storage type string

    Args:
        option: possible storage types (SQLITE, POSTGRES, DUMMY_DATA)

    Returns:
        StorageSource instance based provided option
    """
    storage_types = {
        "SQLITE": StorageSource.SQLITE,
        "POSTGRES": StorageSource.POSTGRES,
        "DUMMY_DATA": StorageSource.DUMMY_DATA
    }

    try:
        storage = storage_types[option]
    except KeyError:
        raise InvalidStorageType(f"Invalid DATABASE_TYPE({option}) provided by .env file")
    else:
        return storage


# Read storage type and define database
STORAGE = read_storage_type(settings.database_type)
if STORAGE == StorageSource.SQLITE:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///src/data/{settings.database_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
if STORAGE == StorageSource.POSTGRES:
    SQLALCHEMY_DATABASE_URL = f"postgresql://willykastner:{settings.database_password}@" \
                              f"localhost:5432/{settings.database_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


# DBSession = sessionmaker(autocommit=False, autoflush=False)
#
# def init_db(file: str):
#     engine = create_engine(file, connect_args={"check_same_thread": False})
#     Base.metadata.bind = engine
#     DBSession.bind = engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    Creates a database session and returns it, while still closing the database session if an error occurs.

    We put the creation of the SessionLocal() and handling of the requests in a try block. And then we close it in the
    "finally" block. This way we make sure the database session is always closed after the request. Even if there was
    an exception while processing the request.

    Returns:
        SQLAlchemy Database session
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def get_repository(storage: StorageSource = STORAGE) -> crud_location.AbstractLocation:
    """
    Factory function that creates the repository instance based on the selected storage.

    - SQLITE: SQLAlchemy ORM to work with SQLite databases
    - POSTGRES: SQLAlchemy ORM to work with Postgres databases
    - DUMMY_DATA: Sample data

    Returns:
        Repository instance based on the selected storage type
    """
    if storage == StorageSource.SQLITE:
        repository = crud_location.SqlAlchemyLocation(db=get_db(), is_sqlite=True)
        return repository
    if storage == StorageSource.POSTGRES:
        repository = crud_location.SqlAlchemyLocation(db=get_db(), is_sqlite=False)
        return repository
    if storage == StorageSource.DUMMY_DATA:
        repository = crud_location.DummyLocation()
        return repository
