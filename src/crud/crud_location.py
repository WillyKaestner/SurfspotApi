from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
import pendulum as pdl

from src.database import schemas
from src.models import models


class AbstractLocation(ABC):

    @abstractmethod
    def add(self, location: schemas.LocationCreate) -> schemas.LocationResponse:
        """Add a location to the storage"""

    @abstractmethod
    def get_by_id(self, location_id: int) -> schemas.LocationResponse:
        """Get a location from the storage by its ID"""

    @abstractmethod
    def get_by_name(self, location_name: str) -> schemas.LocationResponse:
        """Get a location from the storage by its name"""

    @abstractmethod
    def list(self) -> list[schemas.LocationResponse]:
        """List all locations"""

    @abstractmethod
    def update(self, location_id: int, updated_location: schemas.LocationBase) -> schemas.LocationResponse:
        """Update a location in the storage"""

    @abstractmethod
    def delete(self, location_id: int) -> bool:
        """Delete a location in the storage"""


class SqlAlchemyLocation(AbstractLocation):
    """
    SQLAlchemy ORM implementation for handling a database as storage
    """
    def __init__(self, db: Session, is_sqlite: bool):
        self.db = db
        self.is_sqlite = is_sqlite

    def add(self, location: schemas.LocationCreate) -> schemas.LocationResponse:
        if self.is_sqlite:
            db_surfspot = models.MODEL(created_at=pdl.now(tz="UTC"), **location.dict())
        else:
            db_surfspot = models.MODEL(**location.dict())
        self.db.add(db_surfspot)
        self.db.commit()
        self.db.refresh(db_surfspot)
        return db_surfspot

    def get_by_id(self, location_id: int) -> schemas.LocationResponse:
        location_query = self._get_location_by_id_query(location_id)
        return location_query.first()

    def get_by_name(self, location_name: str) -> schemas.LocationResponse:
        return self.db.query(models.MODEL).filter(models.MODEL.name == location_name).first()

    def list(self) -> list[schemas.LocationResponse]:
        return self.db.query(models.MODEL).all()

    def update(self, location_id: int, updated_location: schemas.LocationBase) -> schemas.LocationResponse:
        spot_query = self._get_location_by_id_query(location_id)
        spot_query.update(updated_location.dict(), synchronize_session=False)
        self.db.commit()
        return spot_query.first()

    def delete(self, location_id: int) -> bool:
        location_query = self._get_location_by_id_query(location_id)
        location = location_query.first()

        if location is None:
            return False
        else:
            location_query.delete(synchronize_session=False)
            self.db.commit()
            return True

    def _get_location_by_id_query(self, location_id: int) -> any:
        return self.db.query(models.MODEL).filter(models.MODEL.id == location_id)


class DummyLocation(AbstractLocation):
    """
    Dummy location data for testing
    """
    def add(self, location: schemas.LocationCreate) -> schemas.LocationResponse:
        """Add a location to the storage"""
        dummy_location = schemas.LocationResponse(id=5, created_at=pdl.now(tz="UTC"), **location.dict())
        return dummy_location

    def get_by_id(self, location_id: int) -> schemas.LocationResponse:
        """Get a location from the storage by its ID"""
        dummy_location = schemas.LocationResponse(id=5, name="dummy_location", kitespot=True, surfspot=False,
                                                  created_at=pdl.now(tz="UTC"))
        return dummy_location

    def get_by_name(self, location_name: str) -> schemas.LocationResponse:
        """Get a location from the storage by its name"""
        dummy_location = schemas.LocationResponse(id=5, name="dummy_location", kitespot=True, surfspot=False,
                                                  created_at=pdl.now(tz="UTC"))
        return dummy_location

    def list(self) -> list[schemas.LocationResponse]:
        """List all locations"""
        dummy_location_a = schemas.LocationResponse(id=5, name="dummy_location", kitespot=True, surfspot=False,
                                                    created_at=pdl.now(tz="UTC"))
        dummy_location_b = schemas.LocationResponse(id=6, name="another_location", kitespot=True, surfspot=True,
                                                    created_at=pdl.now(tz="UTC"))
        return [dummy_location_a, dummy_location_b]

    def update(self, location_id: int, updated_location: schemas.LocationBase) -> schemas.LocationResponse:
        """Update a location in the storage"""
        dummy_location = schemas.LocationResponse(id=5, name="updated_dummy_location", kitespot=True, surfspot=False,
                                                  created_at=pdl.now(tz="UTC"))
        return dummy_location

    def delete(self, location_id: int) -> bool:
        """Delete a location in the storage"""
        return True
