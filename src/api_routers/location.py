from fastapi import Response, status, HTTPException, Depends, APIRouter
from src.database import schemas, db_setup
from src.crud import crud_location

router = APIRouter(
    prefix="/location",
    tags=["Locations"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LocationResponse)
def create_spot(location: schemas.LocationCreate,
                storage: crud_location.AbstractLocation = Depends(db_setup.get_repository)):
    location_in_storage = storage.get_by_name(location.name)
    if location_in_storage:
        raise HTTPException(status_code=400, detail="Location already registered")
    return storage.add(location_data=location)


@router.get("/", response_model=list[schemas.LocationResponse])
def read_all_surfspots(storage: crud_location.AbstractLocation = Depends(db_setup.get_repository)):
    locations = storage.list()
    return locations


@router.get("/{location_id}", response_model=schemas.LocationResponse)
def read_surfspot(location_id: int, storage: crud_location.AbstractLocation = Depends(db_setup.get_repository)):
    location = storage.get_by_id(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.put("/{location_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.LocationResponse)
def update_spot(location_id: int,
                updated_location: schemas.LocationBase,
                storage: crud_location.AbstractLocation = Depends(db_setup.get_repository)):
    location = storage.get_by_id(location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id {location_id} does not exist")
    else:
        updated_location_in_storage = storage.update(location_id, updated_location)
        return updated_location_in_storage


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(location_id: int, storage: crud_location.AbstractLocation = Depends(db_setup.get_repository)):
    delete_status = storage.delete(location_id)
    if delete_status is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id {location_id} does not exist")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
