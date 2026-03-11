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

# ─── Pre-commit ───────────────────────────────
hooks-install:
	pre-commit install
	pre-commit install --hook-type commit-msg

# Run hooks against ALL files (not just changed ones)
# Useful first time setup or after adding new hooks
hooks-run:
	pre-commit run --all-files

# Update all hooks to latest versions
hooks-update:
	pre-commit autoupdate

# Skip hooks for ONE commit (use sparingly!)
# Usage: make commit-skip MSG="your message"
commit-skip:
	git commit -m "$(MSG)" --no-verify
