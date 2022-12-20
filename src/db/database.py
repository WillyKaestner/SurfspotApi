from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# TODO perhaps rename to db_setup and rename the package to database or orm

SQLALCHEMY_DATABASE_URL = "sqlite:///src/surfhopper.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# DBSession = sessionmaker(autocommit=False, autoflush=False)
#
# def init_db(file: str):
#     engine = create_engine(file, connect_args={"check_same_thread": False})
#     Base.metadata.bind = engine
#     DBSession.bind = engine

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        print("Database open")
        # yield db
        return db
    finally:
        print("Database closed")
        db.close()


class MySuperContextManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db_context():
    with MySuperContextManager() as db:
        yield db

def get_db_direct():
    db = SessionLocal()
    return db
