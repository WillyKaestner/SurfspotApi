from enum import Enum, auto
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from src.db import schemas, crud, database

router = APIRouter(
    prefix="/location",
    tags=["Locations"]
)

class StorageSource(Enum):
    SQLITE = auto()
    DUMMY_DATA = auto()


# Define Database type tp be used for location
KEYWORD = StorageSource.SQLITE

def get_repository(db: Session = Depends(database.get_db)):
    if KEYWORD == StorageSource.SQLITE:
        # repository = crud.SqlAlchemyRepository(db=db)
        repository = crud.SqlAlchemyRepository(db=database.get_db_direct())
        # repository = get_sql_alchemy_repository()
        return repository
    if KEYWORD == StorageSource.DUMMY_DATA:
        repository = crud.DummyData()
        return repository

# def get_sql_alchemy_repository(db: Session = Depends(database.get_db)):
#     return crud.SqlAlchemyRepository(db=db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LocationResponse)
def create_spot(location: schemas.LocationCreate, storage: crud.AbstractRepository = Depends(get_repository)):
    # db: Session = Depends(database.get_db) # parameter that was removed
    location_in_storage = storage.get_by_name(location.name)
    # db_spot = crud.get_surfspot_by_location(db, location=location.name)
    if location_in_storage:
        raise HTTPException(status_code=400, detail="Location already registered")
    return storage.add(location=location)


@router.get("/", response_model=list[schemas.LocationResponse])
def read_all_surfspots(storage: crud.AbstractRepository = Depends(get_repository)):
    locations = storage.list()
    return locations


@router.get("/{location_id}", response_model=schemas.LocationResponse)
def read_surfspot(location_id: int, storage: crud.AbstractRepository = Depends(get_repository)):
    location = storage.get_by_id(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.put("/{location_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.LocationResponse)
def update_spot(location_id: int,
                updated_location: schemas.LocationBase,
                storage: crud.AbstractRepository = Depends(get_repository)):
    location = storage.get_by_id(location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id {location_id} does not exist")
    else:
        updated_location_in_storage = storage.update(location_id, updated_location)
        return updated_location_in_storage


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(location_id: int, storage: crud.AbstractRepository = Depends(get_repository)):
    delete_status = storage.delete(location_id)
    if delete_status is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id {location_id} does not exist")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
