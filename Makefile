.PHONY: init ci analyze build rebuild migrate lang-make lang-compile

init:
	curl -sSL https://install.python-poetry.org  | python3 -
	poetry install
ci:
	pytest --cov=./
analyze:
	poetry run flake8 .
	poetry run isort -v
reformat:
	black . --exclude 'migrations/'

reformat-check:
	black --check . --exclude 'migrations/'
build:
	docker-compose build
rebuild:
	docker-compose build --force-rm --no-cache
migrate:
	docker-compose run --rm web python manage.py migrate
lang-make:
	poetry run python manage.py makemessages --no-location --no-wrap
lang-compile:
	poetry run python manage.py compilemessages
