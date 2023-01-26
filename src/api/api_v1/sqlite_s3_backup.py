from fastapi import APIRouter
import boto3
from src.config import SETTINGS, DeploymentType, StorageType

router = APIRouter()

# For production on aws lightsail the database is backed up to an S3 data bucket when the application is shut down
if SETTINGS.deployment == DeploymentType.PRODUCTION and SETTINGS.database_type == StorageType.SQLITE:

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
