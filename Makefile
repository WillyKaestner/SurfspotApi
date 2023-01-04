install:
	pip install -r requirements.txt

up:
	uvicorn src.main:app --reload


# DOCKER commands for local development
build_image:
	docker build -t surfspotapi .

start_docker_container:
	docker run -d -p 8000:80 --name surfspotapi_app surfspotapi

delete_docker_container:
	docker stop surfspotapi_app
	docker rm surfspotapi_app


# DOCKER commands for build amd64 images for cloud deployment on linux servers
build_amd64_image:
	docker build --platform linux/amd64 -t surfspotapi_amd64 .

tag_amd64_image:
	docker tag surfspotapi_amd64:latest 720918233027.dkr.ecr.eu-central-1.amazonaws.com/surfspotapi_amd64:latest

push_amd64_image: build_amd64_image tag_amd64_image
	AWS_PROFILE=willy docker push 720918233027.dkr.ecr.eu-central-1.amazonaws.com/surfspotapi_amd64:latest


# Outdated, just for reference
aws_willy_login:
	aws --profile willy ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 720918233027.dkr.ecr.eu-central-1.amazonaws.com

curl_home:
	curl -X GET http://localhost:8000/

curl_create_spot:
	curl -X 'POST' \
	  'http://localhost:8000/spot/' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -d '{"location": "alvor", "kitespot": true, "surfspot": true, "best_tide": "low", "best_wind": "north"}'
