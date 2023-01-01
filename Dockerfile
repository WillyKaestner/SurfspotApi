FROM python:latest

# set the working directory in the docker container
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy all the scripts inside src to the working directory
COPY . /app

# Expose port 8000 & 80
# https://www.cloudbees.com/blog/docker-expose-port-what-it-means-and-what-it-doesnt-mean
# EXPOSE 8000
EXPOSE 80

# start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]

# CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
