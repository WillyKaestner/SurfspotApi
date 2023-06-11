FROM public.ecr.aws/lambda/python:3.10

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
COPY ./src ./src
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
CMD ["src.main.handler"]
