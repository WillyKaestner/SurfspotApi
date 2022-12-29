# SurfSpotAPI
API Application based on FastAPI providing surf and kite spot information

## Local Environment Setup

The following sections cover the steps needed to set up your local environment for working with SurfSpotApi Application.
The steps needed are:
1) [Install dependencies](#install-dependencies)
2) [Create .env file](#create-env-file)
3) [Database setup](#database-setup)
4) [Run local server]()


### Install dependencies

As for the installation of Python dependencies, you can run the following [pip](https://pypi.org/project/pip/) command
```shell
pip install -r requirements.txt
```


### Create .env file

To set up a local .env file:

1) Copy `.env_example` and paste it as `.env` inside the *src/config* directory
2) Replace empty strings in the new .env file with strings containing the secrets

```
DATABASE_TYPE=""
DATABASE_NAME=""
DATABASE_PASSWORD=""
```

Database type options are: *SQLITE, POSTGRES, DUMMY_DATA*. 


### Database setup
Supported databases are SQLite and Postgres databases. A ready to go SQLite database with some sample data is provided 
in `src/data/surfhopper.db`. 

Tables for new databases are created with Alembic migrations. After defining the name of the database in the `.env` 
file, create the database (for sqlite just create a file called `<DATABASE_NAME>.db` in `src/data`) and run the following alembic migration commands:

For SQLite:
```
alembic upgrade c74d6b2647f6
```

For Postgres:
```
alembic upgrade bc993cc2bb84
```

### Run local server
You can run the SurfSpotAPI application using Uvicorn. Get start the application simply run following make command in the terminal
```shell
make up
```
which just calls the underlying uvicorn command
```shell
uvicorn src.main:app --reload
```


More details about how to run a server manually can be found in the [FastAPI documentation](https://fastapi.tiangolo.com/deployment/manually/?h=uvi).


## Debug API application using Insomnia
To debug the application during local development [Insomnia](https://insomnia.rest/) can be used. 
Set up Insomnia [to work with Github](https://docs.insomnia.rest/insomnia/git-sync#enable-git-sync) and connect to the 
repo with the GitHub URI *https://github.com/WillyKaestner/SurfspotApi.git*. Now you got all the commands saved in the repo to debug the application.

Alternatively you can also import the openapi specs saved in the repo at `src/data/openapi.json` or the get
the from FastAPI automatically generated specs from the *http://localhost/openapi.json* endpoint. More details in the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/first-steps/?h=opena#check-the-openapijson)