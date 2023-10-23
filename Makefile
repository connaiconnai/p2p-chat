build:
	docker compose build

up:
	docker compose up -d

buildup:
	@make build
	@make up

init:
	@make buildup
	@make python

down:
	docker compose down


python:
	docker compose exec python3 bash

app:
	docker compose exec python3 sh -c  "python3 app.py"

test:
	docker compose exec python3 sh -c  "python3 test.py"

