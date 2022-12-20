from enum import Enum, auto
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.database import crud


class StorageSource(Enum):
    SQLITE = auto()
    POSTGRES = auto()
    DUMMY_DATA = auto()


# Define Database type tp be used for location
KEYWORD = StorageSource.SQLITE

# Define the Database
SQLALCHEMY_DATABASE_URL = "sqlite:///src/data/surfhopper.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# DBSession = sessionmaker(autocommit=False, autoflush=False)
#
# def init_db(file: str):
#     engine = create_engine(file, connect_args={"check_same_thread": False})
#     Base.metadata.bind = engine
#     DBSession.bind = engine

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    Creates a database session and returns it, while still closing the database session if an error occurs.

    Returns:
        SQLAlchemy Database session
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def get_repository() -> crud.AbstractRepository:
    """
    Factory function that creates the repository instance based on the selected storage.

    - SQLITE: SQLAlchemy ORM to work with SQLite databases
    - POSTGRES: SQLAlchemy ORM to work with Postgres databases
    - DUMMY_DATA: Sample data

    Returns:
        Repository instance based on the selected storage type
    """
    if KEYWORD == StorageSource.SQLITE:
        repository = crud.SqlAlchemyRepository(db=get_db(), is_sqlite=True)
        return repository
    if KEYWORD == StorageSource.POSTGRES:
        repository = crud.SqlAlchemyRepository(db=get_db(), is_sqlite=False)
        return repository
    if KEYWORD == StorageSource.DUMMY_DATA:
        repository = crud.DummyData()
        return repository
