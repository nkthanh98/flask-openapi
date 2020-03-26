lint:
	pylint-fail-under --fail_under 9.5 app

test:
	make lint
	pytest
