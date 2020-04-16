test:
	python -m pytest

lint:
	PYTHONPATH=. python linter.py --fail-under 9.5 app

build:
	docker-compose build

run:
	docker-compose up -d

start:
	make build
	make run

stop:
	docker-compose stop

clean:
	@rm -rf coverage.xml .coverage htmlcov
	docker-compose stop
	docker-compose rm
