from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
import pendulum as pdl

import src.schemas as schemas
import src.models as models


class AbstractLocation(ABC):

    @abstractmethod
    def add(self, location_data: schemas.LocationCreate) -> schemas.LocationResponse:
        """Add a location to the storage"""

    @abstractmethod
    def get_by_id(self, location_id: int) -> schemas.LocationResponse | None:
        """Get a location from the storage by its ID"""

    @abstractmethod
    def get_by_name(self, location_name: str) -> schemas.LocationResponse | None:
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

    def add(self, location_data: schemas.LocationCreate) -> schemas.LocationResponse:
        db_surfspot = self._create_data_model(location_data)
        self.db.add(db_surfspot)
        self.db.commit()
        self.db.refresh(db_surfspot)
        return db_surfspot

    def get_by_id(self, location_id: int) -> schemas.LocationResponse | None:
        location_query = self._get_location_by_id_query(location_id)
        return location_query.first()

    def get_by_name(self, location_name: str) -> schemas.LocationResponse | None:
        return self.db.query(models.Location).filter(models.Location.name == location_name).first()

    def list(self) -> list[schemas.LocationResponse]:
        return self.db.query(models.Location).all()

    def update(self, location_id: int, updated_location: schemas.LocationBase) -> schemas.LocationResponse:
        spot_query = self._get_location_by_id_query(location_id)
        spot_query.update(updated_location.dict(), synchronize_session=False)
        self.db.commit()
        return spot_query.first()

    def delete(self, location_id: int) -> bool:
        location_query = self._get_location_by_id_query(location_id)
        location_data = location_query.first()

        if location_data is None:
            return False
        else:
            location_query.delete(synchronize_session=False)
            self.db.commit()
            return True

    def _create_data_model(self, location_data: schemas.LocationCreate) -> models.Location:
        """Create the data model instance populated with the location details to be added to the database"""
        if self.is_sqlite:
            db_surfspot = models.Location(created_at=pdl.now(tz="UTC"), **location_data.dict())
        else:
            db_surfspot = models.Location(**location_data.dict())
        return db_surfspot

    def _get_location_by_id_query(self, location_id: int) -> any:
        return self.db.query(models.Location).filter(models.Location.id == location_id)


class DummyLocation(AbstractLocation):
    """
    Dummy location data for testing
    """
    def add(self, location_data: schemas.LocationCreate) -> schemas.LocationResponse:
        """Add a location to the storage"""
        dummy_location = schemas.LocationResponse(id=5, created_at=pdl.now(tz="UTC"), **location_data.dict())
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


class FakeDB(AbstractLocation):
    """
    Dummy location data for testing
    """
    fake_db = [
        {
            "id": 1,
            "name": "Mos",
            "kitespot": True,
            "surfspot": True,
            "best_tide": "low to mid",
            "best_wind": "north-west to south",
            "created_at": pdl.now(tz="UTC")
        },
        {
            "id": 2,
            "name": "Alvor",
            "kitespot": True,
            "surfspot": False,
            "best_tide": "all tides",
            "best_wind": "north-west and south-east",
            "created_at": pdl.now(tz="UTC")
        },
        {
            "id": 3,
            "name": "Ingrina",
            "kitespot": False,
            "surfspot": True,
            "best_tide": "low to mid",
            "best_wind": "north",
            "created_at": pdl.now(tz="UTC")
        },
    ]

    def add(self, location_data: schemas.LocationCreate) -> schemas.LocationResponse:
        new_id = FakeDB.fake_db[-1]["id"] + 1
        location_data = schemas.LocationResponse(id=new_id, **location_data.dict(), created_at=pdl.now(tz="UTC"))
        FakeDB.fake_db.append(location_data.dict())
        return location_data

    def get_by_id(self, location_id: int) -> schemas.LocationResponse | None:
        for item in FakeDB.fake_db:
            if location_id == item["id"]:
                return schemas.LocationResponse(**item)

        return None

    def get_by_name(self, location_name: str) -> schemas.LocationResponse | None:
        for item in FakeDB.fake_db:
            if location_name == item["name"]:
                return schemas.LocationResponse(**item)

        return None

    def list(self) -> list[schemas.LocationResponse]:
        response_list = []
        for item in FakeDB.fake_db:
            response_list.append(schemas.LocationResponse(**item))
        return response_list

    def update(self, location_id: int, updated_location: schemas.LocationBase) -> schemas.LocationResponse:
        for index, item in enumerate(FakeDB.fake_db):
            if location_id == item["id"]:
                location_data = schemas.LocationResponse(id=location_id,
                                                         **updated_location.dict(),
                                                         created_at=pdl.now(tz="UTC"))
                FakeDB.fake_db[index] = location_data.dict()
                return location_data

    def delete(self, location_id: int) -> bool:
        for index, item in enumerate(FakeDB.fake_db):
            if location_id == item["id"]:
                FakeDB.fake_db.pop(index)
                return True
        return False
