BASE_TAG = travel-base
RUN_LEVEL = dev

build:
	docker build -t $(BASE_TAG) -f ./service/deployment/docker/Dockerfile  --build-arg RUN_LEVEL=$(RUN_LEVEL) ./service
	docker-compose build --build-arg BASE_TAG=$(BASE_TAG)
