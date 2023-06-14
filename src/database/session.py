from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config import SETTINGS, StorageType

def create_db_engine():
    """Create and return database engine based on the storage defined in config"""
    if SETTINGS.database_type == StorageType.SQLITE:
        engine = create_engine(get_database_url(), connect_args={"check_same_thread": False})
        return engine

    if SETTINGS.database_type == StorageType.POSTGRES:
        engine = create_engine(get_database_url())
        return engine

def get_database_url() -> str:
    """Return the database base url generated according to config"""
    if SETTINGS.database_type == StorageType.SQLITE:
        sqlalchemy_database_url = f"sqlite:///./src/data/{SETTINGS.database_name}"
    elif SETTINGS.database_type == StorageType.POSTGRES:
        sqlalchemy_database_url = f"postgresql://{SETTINGS.database_username}:{SETTINGS.database_password}@" \
                                  f"{SETTINGS.database_host}:{SETTINGS.database_port}/{SETTINGS.database_name}"
    else:
        raise ValueError(f"Couldn't create database url because of invalid storage type: {SETTINGS.database_type.name}")
    return sqlalchemy_database_url


def get_db() -> Session:
    """
    Creates a database session and returns it, while still closing the database session if an error occurs.

    We put the creation of the sessionlocal() and handling of the requests in a try block. And then we close it in the
    "finally" block. This way we make sure the database session is always closed after the request. Even if there was
    an exception while processing the request.

    Returns:
        SQLAlchemy Database session
    """
    engine = create_db_engine()
    sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = sessionlocal()
    try:
        return db
    finally:
        db.close()
