up:
	docker compose up --build

fast-up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f

worker:
	docker compose logs -f worker

api:
	docker compose logs -f api

redis:
	docker compose logs -f redis

shell:
	docker compose exec api bash

lint:
	ruff check . --fix
