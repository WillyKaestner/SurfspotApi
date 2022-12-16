FROM python:latest

# set the working directory in the docker container
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy all the scripts inside src to the working directory
COPY . /app

# start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]