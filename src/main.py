import logging.config
import functools
import io
import yaml
from fastapi import FastAPI, Response
from mangum import Mangum

from src.config.logging_config import LOGGING_CONFIG
import src.database as db
from src.api.api_v1.api import api_router
from src.config import SETTINGS, StorageType

# TODO: implement authorization
# TODO: change Githubs actions pipeline to reuse steps (testing)
# TODO: create a Github actions deployment that only works on testing branches -> for trying out deployment options
# TODO: add testing
# TODO: add CORS
# TODO: add location_online endpoints that triggers a crawler to fetch data from somewhere
#  (msw, google, openstreetmaps etc)

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info(f"Application started with the following settings. Deployment type:{SETTINGS.deployment}. "
            f"Database type: {SETTINGS.database_type}. Database: {SETTINGS.database_name}")


# Create SQLite database (for Postgres the database has to already exist) and tables if they don't exist yet
if SETTINGS.database_type == StorageType.SQLITE:
    db.init_db()

# @app.on_event("startup")
# async def start_up_event():
#     db.init_db(db.DB_FILE)


# Create FastAPI app and include routers
app = FastAPI()
app.include_router(api_router)

@app.get("/")
async def root():
    logger.info("Root endpoint successfully loaded")
    return "Hello World - Surfspot & Kitespot server is running"


# additional yaml version of openapi.json
# https://github.com/tiangolo/fastapi/issues/1140
@app.get('/openapi.yaml', include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml() -> Response:
    openapi_json = app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type='text/yaml')


# save open api documentation as json file
# file_path = Path(__file__).parent / 'data' / 'openapi_doc.json'
# openapi_doc = app.openapi()
# with open(file_path, "w") as outfile:
#     json.dump(openapi_doc, outfile)

###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

