from fastapi import FastAPI, Response
import functools
import io
import yaml
import src.database as db
from src.api.api_v1.api import api_router
from src.config import SETTINGS, StorageType

# TODO: implement authorization
# TODO: add testing
# TODO: add CORS
# TODO: add location_online endpoints that triggers a crawler to fetch data from somewhere
#  (msw, google, openstreetmaps etc)


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
