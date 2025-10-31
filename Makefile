SCOPE=src/

.PHONY: format lint test clear-postgres run-pgpx-postgres


format:
	uv run ruff format $(SCOPE)
	uv run ruff check --fix --exit-zero $(SCOPE)

lint:
	uv run ruff check $(SCOPE)
	uv run ruff format --check $(SCOPE)

clear-postgres:
	docker rm -f pgpx-postgres || true

run-pgpx-postgres:
	docker run -d --name pgpx-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:17

test: clear-postgres run-pgpx-postgres
	@echo "Waiting for PostgreSQL to be ready..."
	@until docker exec pgpx-postgres pg_isready -U postgres > /dev/null 2>&1; do sleep 1; done
	uv run python -m unittest discover tests