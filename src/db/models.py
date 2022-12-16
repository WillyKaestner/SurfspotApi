from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()


class DBSurfHopper(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    kitespot = Column(Boolean, nullable=False)
    surfspot = Column(Boolean, nullable=False)
    best_wind = Column(String, nullable=False)
    best_tide = Column(String, nullable=False)
    wave_info = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
