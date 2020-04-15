test:
	python -m pytest

lint:
	PYTHONPATH=. python linter.py --fail-under 9.5 app

serve:
	docker-compose build
	docker-compose up -d

start:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose stop

clean:
	@rm -rf coverage.xml .coverage htmlcov
	docker rmi flask-app-unittest
	docker-compose rm
