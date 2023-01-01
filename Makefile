install:
	pip install -r requirements.txt

up:
	uvicorn src.main:app --reload

curl_home:
	curl -X GET http://localhost:8000/

curl_create_spot:
	curl -X 'POST' \
	  'http://localhost:8000/spot/' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -d '{"location": "alvor", "kitespot": true, "surfspot": true, "best_tide": "low", "best_wind": "north"}'


build_docker_image:
	docker build -t surfspotapi .

start_docker_container:
	docker run -d -p 8000:8000 --name surfspotapi_app surfspotapi

delete_docker_container:
	docker stop surfspotapi_app
	docker rm surfspotapi_app

aws_willy_login:
	aws --profile willy ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 720918233027.dkr.ecr.eu-central-1.amazonaws.com
