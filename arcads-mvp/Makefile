SHELL := /usr/bin/bash

.PHONY: docker-up docker-down docker-logs backend frontend

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v

docker-logs:
	docker compose logs -f

backend:
	bash scripts/run-backend.sh

frontend:
	cd frontend && npm install && npm run dev