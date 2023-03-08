FROM public.ecr.aws/lambda/python:3.10

# Set ENV variables for CI/CD
ARG ARG_DATABASE_TYPE
ARG ARG_DATABASE_NAME
ARG ARG_DEPLOYMENT
ARG ARG_DATABASE_PASSWORD
ARG ARG_DATABASE_USERNAME
ARG ARG_DATABASE_HOST
ARG ARG_AWS_ACCESS_KEY_ID
ARG ARG_AWS_SECRET_ACCESS_KEY

ENV DATABASE_TYPE=$ARG_DATABASE_TYPE
ENV DATABASE_NAME=$ARG_DATABASE_NAME
ENV DEPLOYMENT=$ARG_DEPLOYMENT
ENV DATABASE_PASSWORD=$ARG_DATABASE_PASSWORD
ENV DATABASE_USERNAME=$ARG_DATABASE_USERNAME
ENV DATABASE_HOST=$ARG_DATABASE_HOST
ENV AWS_ACCESS_KEY_ID=$ARG_AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$ARG_AWS_SECRET_ACCESS_KEY

## Set the working directory in the docker container
#WORKDIR /app
#
## Install dependencies
#COPY ./requirements.txt /app
#RUN pip install --no-cache-dir --upgrade -r requirements.txt
#
## Copy all the scripts inside src to the working directory
#COPY . /app
#
## Expose port 80
## https://www.cloudbees.com/blog/docker-expose-port-what-it-means-and-what-it-doesnt-mean
#EXPOSE 80
#
## Point to mangum handler for aws lambda entrypoint
## CMD ["src.main.handler"]
#CMD ["app.src.main.handler"]

# From Tut
COPY ./src ./app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
CMD ["app.main.handler"]