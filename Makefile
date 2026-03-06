# ─── Setup ───────────────────────────────────
setup:
	cp backend/.env.example backend/.env
	cp frontend/.env.example frontend/.env
	pre-commit install

# ─── Development ─────────────────────────────
up:
	docker compose up

up-build:
	docker compose up --build

down:
	docker compose down

# ─── Logs ────────────────────────────────────
logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-frontend:
	docker compose logs -f frontend

# ─── Django Commands ─────────────────────────
migrate:
	docker compose exec backend python manage.py migrate

makemigrations:
	docker compose exec backend python manage.py makemigrations

shell:
	docker compose exec backend python manage.py shell

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

# ─── Testing ─────────────────────────────────
test-backend:
	docker compose exec backend pytest

test-frontend:
	docker compose exec frontend npm test

test-all:
	make test-backend
	make test-frontend

# ─── Database ────────────────────────────────
db-shell:
	docker compose exec db psql -U ${DB_USER} -d ${DB_NAME}

# ─── Cleanup ─────────────────────────────────
clean:
	docker compose down -v --remove-orphans

prune:
	docker system prune -af --volumes