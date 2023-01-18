from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every
import boto3
from src.config import SETTINGS, DeploymentType

router = APIRouter()

# For production on aws lightsail the database is backed up to an S3 data bucket when the application is shut down
if SETTINGS.deployment == DeploymentType.PRODUCTION:

    s3 = boto3.client("s3",
                      region_name='eu-central-1',
                      aws_access_key_id=SETTINGS.aws_access_key_id,
                      aws_secret_access_key=SETTINGS.aws_secret_access_key)

    @router.on_event("startup")
    async def get_sqlite_db_from_s3():
        """Download sqlite database backup from AWS S3 during startup of the server"""
        with open('./src/data/surfhopper.db', 'wb') as f:
            s3.download_fileobj('surfspotapi-sqlite-db', 'surfhopper.db', f)
            print("Downloaded surfhopper.db from s3 object")

    @router.on_event("shutdown")
    @repeat_every(seconds=60 * 60)  # every 1 hour
    async def backup_sqlite_db_to_s3():
        """Upload sqlite database to AWS S3 when server is shut down"""
        with open("./src/data/surfhopper.db", "rb") as f:
            s3.upload_fileobj(f, "surfspotapi-sqlite-db", "surfhopper.db")
            print("Uploaded surfhopper.db s3 object")

