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
