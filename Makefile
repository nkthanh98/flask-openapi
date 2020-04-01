lint:
	pylint-fail-under --fail_under 9.5 app

test:
	@export PYTHONPATH=$(pwd)
	@export ENVIRONMENT=testing
	@pytest

serve:
	gunicorn wsgi:application --bind "0.0.0.0:80" --worker-class gevent

clean:
	@rm -rf coverage.xml .coverage htmlcov
