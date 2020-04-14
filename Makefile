test:
	docker build . -t flask-app-unittest -f unit-test.dockerfile
	docker run -it --rm flask-app-unittest

build:
	docker-compose build

serve:
	docker-compose up -d

start:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose stop

clean:
	docker rmi flask-app-unittest
