from fastapi import Response, status, HTTPException, Depends, APIRouter, BackgroundTasks
import src.schemas as schemas
from src.crud import crud_location, repository
from src.config import SETTINGS, DeploymentType
import boto3

router = APIRouter(
    prefix="/location",
    tags=["Locations"]
)

def backup_sqlite_to_s3():
    """Upload sqlite database to AWS S3 when server is shut down"""
    print("sqlite backup function triggered")
    with open("./src/data/surfhopper.db", "rb") as f:
        s3 = boto3.client("s3",
                          region_name='eu-central-1',
                          aws_access_key_id=SETTINGS.aws_access_key_id,
                          aws_secret_access_key=SETTINGS.aws_secret_access_key)
        s3.upload_fileobj(f, "surfspotapi-sqlite-db", "surfhopper.db")
        print("Uploaded surfhopper.db s3 object")

@router.post("/backup", status_code=status.HTTP_202_ACCEPTED)
def backup_location_db():
    if SETTINGS.deployment == DeploymentType.PRODUCTION:
        print("post endpoint triggered and production set")
        backup_sqlite_to_s3()
    else:
        raise HTTPException(status_code=400, detail="Not a production setup")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LocationResponse)
def create_spot(location: schemas.LocationCreate,
                background_tasks: BackgroundTasks,
                storage: crud_location.AbstractLocation = Depends(repository.get_crud_location)):
    location_in_storage = storage.get_by_name(location.name)
    if location_in_storage:
        raise HTTPException(status_code=400, detail="Location already registered")
    location_response = storage.add(location_data=location)
    # Backup database in production
    if SETTINGS.deployment == DeploymentType.PRODUCTION:
        print("post endpoint triggered and production set")
        background_tasks.add_task(backup_sqlite_to_s3)
    return location_response


@router.get("/", response_model=list[schemas.LocationResponse])
def read_all_surfspots(storage: crud_location.AbstractLocation = Depends(repository.get_crud_location)):
    locations = storage.list()
    return locations


@router.get("/{location_id}", response_model=schemas.LocationResponse)
def read_surfspot(location_id: int, storage: crud_location.AbstractLocation = Depends(repository.get_crud_location)):
    location = storage.get_by_id(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.put("/{location_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.LocationResponse)
def update_spot(location_id: int,
                updated_location: schemas.LocationBase,
                storage: crud_location.AbstractLocation = Depends(repository.get_crud_location)):
    location = storage.get_by_id(location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id {location_id} does not exist")
    else:
        updated_location_in_storage = storage.update(location_id, updated_location)
        return updated_location_in_storage


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(location_id: int, storage: crud_location.AbstractLocation = Depends(repository.get_crud_location)):
    delete_status = storage.delete(location_id)
    if delete_status is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Location with id {location_id} does not exist")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
