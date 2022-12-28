from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from src.config import SETTINGS, StorageType
from src.models.base_class import Base


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    kitespot = Column(Boolean, nullable=False)
    surfspot = Column(Boolean, nullable=False)
    best_wind = Column(String)
    best_tide = Column(String)
    wave_info = Column(String)
    if SETTINGS.database_type == StorageType.SQLITE:
        created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    else:
        created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# def get_sqlite_location_model():
#     class LocationModelSQLite(Base):
#         __tablename__ = "locations"
#         id = Column(Integer, primary_key=True, autoincrement=True)
#         name = Column(String, nullable=False)
#         kitespot = Column(Boolean, nullable=False)
#         surfspot = Column(Boolean, nullable=False)
#         best_wind = Column(String)
#         best_tide = Column(String)
#         wave_info = Column(String)
#         created_at = Column(TIMESTAMP(timezone=True), nullable=False)
#     return LocationModelSQLite
#
#
# def get_postgres_location_model():
#     class LocationModelPostgres(Base):
#         __tablename__ = "locations"
#         id = Column(Integer, primary_key=True, autoincrement=True)
#         name = Column(String, nullable=False)
#         kitespot = Column(Boolean, nullable=False)
#         surfspot = Column(Boolean, nullable=False)
#         best_wind = Column(String)
#         best_tide = Column(String)
#         wave_info = Column(String)
#         created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#     return LocationModelPostgres
#
# else:
#     class Location:
#         print("EMPTY LOCATION MODEL CREATED - ONLY FOR DUMMY DATA")
#         pass
#
# MODEL = Location
