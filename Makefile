.PHONY: all build_base build_web build_worker push_base push_web push_worker

all: build_base push_base build_web push_web build_worker push_worker

build_base:
	docker build -f ./dockerfiles/Dockerfile.base -t cade/donate-locust:base-latest .

push_base:
	docker push cade/donate-locust:base-latest

build_web:
	docker build -f ./dockerfiles/Dockerfile.web -t cade/donate-locust:web-latest .

push_web:
	docker push cade/donate-locust:web-latest

build_worker:
	docker build -f ./dockerfiles/Dockerfile.worker -t cade/donate-locust:worker-latest .

push_worker:
	docker push cade/donate-locust:worker-latest