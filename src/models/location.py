from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from src.config import SETTINGS, StorageType

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


if SETTINGS.database_type == StorageType.SQLITE:
    MODEL = SQLiteLocation
if SETTINGS.database_type == StorageType.POSTGRES:
    MODEL = PostgresLocation
