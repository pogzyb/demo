build-and-run:
	docker-compose up --build

build-and-tag:
	docker-compose build
	docker tag simple-api_search-api:latest search-api:0.1.0

test:
	docker-compose up -d
	docker exec -it search-api pytest
	docker-compose down

run:
	docker-compose up
