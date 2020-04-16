test:
	python -m pytest

lint:
	PYTHONPATH=. python linter.py --fail-under 9.5 app

clean:
	@rm -rf coverage.xml .coverage htmlcov
