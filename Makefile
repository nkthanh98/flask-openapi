test:
	docker build . -t flask-app-unittest -f unittest.dockerfile
	docker run -it --rm ${ci_env} flask-app-unittest

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
	docker-compose rm
