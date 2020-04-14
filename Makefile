lint:
	PYTHONPATH=. python linter.py --fail_under 9.5 app

test:
	pytest

serve:
	gunicorn wsgi:application --bind "0.0.0.0:5000" --worker-class gevent

clean:
	@rm -rf coverage.xml .coverage htmlcov
