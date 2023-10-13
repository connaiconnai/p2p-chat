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


python:
	docker compose exec python3 bash
