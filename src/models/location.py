from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from src.config import SETTINGS, StorageType
from src.models.base_class import Base


if SETTINGS.database_type == StorageType.SQLITE:
    class Location(Base):
        __tablename__ = "locations"
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String, nullable=False)
        kitespot = Column(Boolean, nullable=False)
        surfspot = Column(Boolean, nullable=False)
        best_wind = Column(String)
        best_tide = Column(String)
        wave_info = Column(String)
        created_at = Column(TIMESTAMP(timezone=True), nullable=False)


if SETTINGS.database_type == StorageType.POSTGRES:
    class Location(Base):
        __tablename__ = "locations"
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String, nullable=False)
        kitespot = Column(Boolean, nullable=False)
        surfspot = Column(Boolean, nullable=False)
        best_wind = Column(String)
        best_tide = Column(String)
        wave_info = Column(String)
        created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

MODEL = Location
