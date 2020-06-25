test:
	python -m pytest

lint:
	PYTHONPATH=. python linter.py --fail-under 9.5 app

compile:
	python setup.py build_ext --inplace

clean:
	@rm -rf coverage.xml .coverage htmlcov
