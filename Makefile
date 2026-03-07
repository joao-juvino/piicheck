run:
	pipenv run python run.py

migrate:
	pipenv run flask db migrate

upgrade:
	pipenv run flask db upgrade

init-db:
	pipenv run flask db init