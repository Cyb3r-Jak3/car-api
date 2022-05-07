PHONY: lint format test


lint:
	black --check app
	pylint app
	flake8 --statistics --show-source --count app
	bandit -r app

format:
	black app

test:
	pytest --cov -v