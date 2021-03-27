BASE_TAG = travel-base

build:
	docker build -t $(BASE_TAG) -f ./service/deployment/docker/Dockerfile ./service
	docker-compose build --build-arg BASE_TAG=$(BASE_TAG)
