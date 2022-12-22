from fastapi import FastAPI, Response
import functools
import io
import yaml

from .database.db_setup import engine
from src.models.location import Base
from .api_routers import location

# TODO: implement authorization
# TODO: add testing
# TODO: add alembic
# TODO: create a simple readme file
# TODO: try out with postgres database

# DONE TODO's
# TODO: add api_routers to clean up this main file -> create location.py and move everything connected there
# TODO: create git and github repo
# TODO: create a config file that reads in specific deployment values (which kind of database to use etc.)
# TODO: create option here to work with SQLite or Postgres Database (perhaps even just a list etc.)
#  This can probably be done in a way that the location api endpoints (get, post etc) don't rely on a concrete
#  implementation but rather an interface to preform their crud actions

# create the tables in the database, based on the sqlalchemy models
Base.metadata.create_all(bind=engine)

# Create FastAPI app and include routers
app = FastAPI()
app.include_router(location.router)


# @app.on_event("startup")
# async def start_up_event():
#     db.init_db(db.DB_FILE)

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
