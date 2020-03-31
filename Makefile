test:
	python -m pytest

lint:
	PYTHONPATH=. python linter.py --fail-under 9.5 app

start:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose stop

clean:
	@rm -rf coverage.xml .coverage htmlcov
	docker-compose stop
	docker-compose rm
