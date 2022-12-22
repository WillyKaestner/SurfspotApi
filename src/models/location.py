from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

Base = declarative_base()

class SQLiteLocation(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    kitespot = Column(Boolean, nullable=False)
    surfspot = Column(Boolean, nullable=False)
    best_wind = Column(String)
    best_tide = Column(String)
    wave_info = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)


class PostgresLocation(Base):
    __tablename__ = "locations"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    kitespot = Column(Boolean, nullable=False)
    surfspot = Column(Boolean, nullable=False)
    best_wind = Column(String)
    best_tide = Column(String)
    wave_info = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# STORAGE = db_setup.STORAGE
# if STORAGE == db_setup_a.StorageSource.SQLITE:
#     MODEL = SQLiteLocation
# if STORAGE == db_setup_a.StorageSource.POSTGRES:
#     MODEL = PostgresLocation

MODEL = PostgresLocation

