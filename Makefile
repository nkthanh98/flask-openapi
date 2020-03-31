lint:
	pylint-fail-under --fail_under 9.5 app

test:
	@export PYTHONPATH=$(pwd)
	@export ENVIRONMENT=testing
	@pytest

clean:
	@rm -rf coverage.xml .coverage htmlcov
