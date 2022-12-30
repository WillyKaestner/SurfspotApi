from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config import SETTINGS, StorageType


# Create Base Session (SessionLocal) based on the Storage selected
if SETTINGS.database_type == StorageType.SQLITE:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./src/data/{SETTINGS.database_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
elif SETTINGS.database_type == StorageType.POSTGRES:
    SQLALCHEMY_DATABASE_URL = f"postgresql://willykastner:{SETTINGS.database_password}@" \
                              f"localhost:5432/{SETTINGS.database_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

else:
    # Only needed for Dummy_Data so that no errors are raised when importing engine in init_db.py
    engine = None


#TODO: Errorhandling if engine couldn't be created for some reason?


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
