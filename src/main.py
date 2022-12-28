from fastapi import FastAPI, Response
import functools
import io
import yaml
import src.database as db
from src.api.api_v1.api import api_router
from src.config import SETTINGS, StorageType

# TODO: implement authorization
# TODO: add testing

# DONE TODO's
# TODO: add api_routers to clean up this main file -> create location.py and move everything connected there
# TODO: create git and github repo
# TODO: create a config file that reads in specific deployment values (which kind of database to use etc.)
# TODO: create option here to work with SQLite or Postgres Database (perhaps even just a list etc.)
#  This can probably be done in a way that the location api endpoints (get, post etc) don't rely on a concrete
#  implementation but rather an interface to preform their crud actions
# TODO: try out with postgres database
# TODO: use enums for handling the database types
# TODO: add validation to the pydantic model when reading in the database type
# TODO: Find a better solution for creating a database engine & SessionLocal instance so it is skipped when working
#  with Dummy_Data
# TODO: create a simple readme file
# TODO: add alembic

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
