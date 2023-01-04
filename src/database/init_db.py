import src.models as models
from src.database.session import create_db_engine


# make sure all SQL Alchemy models are imported (src.database.base) before initializing DB otherwise, SQL Alchemy
# might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    models.Base.metadata.create_all(bind=create_db_engine())
