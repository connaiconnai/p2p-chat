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

app:
	docker compose exec python3 sh -c "python3 app.py"

server:
	docker compose exec python3 sh -c "python3 server.py"

client:
	docker compose exec python3 sh -c "python3 client.py"
