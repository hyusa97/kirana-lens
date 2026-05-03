.PHONY: help dev migrate revision test install clean

help:
	@echo "KiranaLens API - Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Run development server"
	@echo "  make migrate    - Run database migrations"
	@echo "  make revision   - Create new migration (use: make revision msg='description')"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean Python cache files"

install:
	pip install -r requirements.txt

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

migrate:
	alembic upgrade head

revision:
	@if [ -z "$(msg)" ]; then \
		echo "Error: Please provide a message. Usage: make revision msg='your message'"; \
		exit 1; \
	fi
	alembic revision --autogenerate -m "$(msg)"

test:
	pytest -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.py~" -delete
