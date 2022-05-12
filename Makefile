PHONY: lint format test


lint:
	black --check app
	pylint app --load-plugins pylint_flask_sqlalchemy
	flake8 --statistics --show-source --max-line-length 100 --count app
	bandit -r app

format:
	black app

test:
	python -m pytest --cov -v