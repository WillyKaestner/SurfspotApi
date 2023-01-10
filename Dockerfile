FROM python:latest

# Set ENV variables for CI/CD
ARG ARG_DATABASE_TYPE
ARG ARG_DATABASE_NAME
ENV DATABASE_TYPE=$ARG_DATABASE_TYPE
ENV DATABASE_NAME=$ARG_DATABASE_NAME

# Set the working directory in the docker container
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy all the scripts inside src to the working directory
COPY . /app

# Expose port 80
# https://www.cloudbees.com/blog/docker-expose-port-what-it-means-and-what-it-doesnt-mean
EXPOSE 80

# start the server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
