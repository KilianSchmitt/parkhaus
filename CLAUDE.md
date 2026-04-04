# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **FastAPI-based REST/GraphQL API** for a parking garage management system ("Parkhaus"). It is an educational project using modern Python practices with SQLAlchemy ORM, PostgreSQL, and Keycloak authentication.

## Common Commands

### Development Server
```bash
# Run the application with uvicorn (uses .venv)
uv run parkhaus

# Alternative: Run as a Python module
uv run python -m parkhaus

# Run with FastAPI dev mode (auto-reload)
uv run fastapi dev src/parkhaus
```

### Database & Infrastructure
```bash
# Start PostgreSQL and Keycloak via Docker Compose
# (see extras/compose/ for compose files)
docker-compose -f extras/compose/postgres/compose.yml up -d
docker-compose -f extras/compose/keycloak/compose.yml up -d
```

### Testing
```bash
# Run all tests with coverage and HTML report
uv run pytest

# Run only REST tests
uv run pytest -m rest

# Run specific test by name
uv run pytest -k test_post_invalid_json

# Run single test file
uv run pytest tests/unit/test_parkhaus.py

# Run without coverage (faster)
uv run pytest --no-cov
```

### Code Quality
```bash
# Lint with ruff (with auto-fix)
uvx ruff check --fix src tests

# Format code
uvx ruff format src tests

# Type checking with ty
uvx ty check src tests
```

### Dependency Management
```bash
# Sync dependencies after updating pyproject.toml
uv sync --all-groups

# Show dependency tree
uv tree

# Check for outdated packages
uv tree --outdated --all-groups --depth=1

# Export lock file (PEP 751)
uv export -o pylock.toml
```

### Documentation
```bash
# Serve MkDocs documentation locally
uv run mkdocs serve
```

### Load Testing
```bash
# Run Locust load tests
uvx locust -f extras/locustfile.py
```

## Architecture Overview

### Layer Structure

The codebase follows a **layered architecture** under `src/parkhaus/`:

```
config/          # Configuration (TOML-based)
  resources/     # SQL files, TLS certs, app.toml
  dev/           # Dev-only utilities (DB population)
entity/          # SQLAlchemy ORM models (Parkhaus, Auto, Adresse)
repository/      # Data access layer (ParkhausRepository, Session factory)
service/         # Business logic layer (ParkhausService, DTOs)
router/          # FastAPI route handlers (REST API)
```

### Key Components

**Entry Points:**
- `__main__.py` - Module entry point
- `asgi_server.py` - Uvicorn server startup with TLS support
- `fastapi_app.py` - FastAPI app factory with lifespan management

**Domain Model:**
- `Parkhaus` (aggregate root) 1:1 with `Adresse`
- `Parkhaus` 1:N with `Auto`
- Optimistic locking via `version` field
- Entities: See `src/parkhaus/entity/`

**Data Flow:**
```
HTTP Request → Router → Service → Repository → SQLAlchemy → PostgreSQL
```

- **Router**: Pydantic models for validation, dependency injection via `dependencies.py`
- **Service**: Transaction boundary with `Session()` context manager
- **Repository**: SQLAlchemy queries with eager loading (`joinedload`)

### Configuration

Configuration is loaded from `src/parkhaus/config/resources/app.toml` at startup:
- Database: PostgreSQL connection (default: localhost:5432)
- TLS: Certificate and key files for HTTPS
- Keycloak: OAuth2/OIDC authentication
- Dev flags: `db-populate`, `keycloak-populate` for test data

**Important**: The app uses `dev_db_populate` flag (from `config/dev_modus.py`) to reload the database with test data on startup in development mode.

### Testing Markers

Tests use pytest markers (defined in `pyproject.toml`):
- `rest` - REST API tests
- `get_request`, `post_request`, `put_request`, `delete_request` - HTTP method specific
- `login` - Authentication tests
- `health` - Health check endpoints
- `graphql` - GraphQL tests
- `unit`, `unit_find_by_id`, `unit_create` - Unit test categories

### External Services

- **PostgreSQL**: Database with SSL/TLS support (see `config/db.py`)
- **Keycloak**: OAuth2/OIDC authentication (configured in `config/keycloak.py`)
- **Prometheus**: Metrics via `prometheus-fastapi-instrumentator`

### Dependencies

- **Package Manager**: `uv` (not pip)
- **Python Version**: 3.14.3+
- **Key Libraries**: FastAPI, SQLAlchemy 2.0, Pydantic v2, psycopg3, loguru, strawberry-graphql

## Project Conventions

- **Language**: German (domain terms like "Parkhaus", "Kennzeichen", "Kundentyp")
- **Docstrings**: Google-style with type hints
- **Types**: Strict typing with `Final`, `Annotated`, `| None` union syntax
- **Linting**: Ruff with FastAPI-specific rules (`FAST`)
- **Import**: Absolute imports from `parkhaus` package, `__all__` defined in modules

## Bruno API Testing

The `extras/bruno/` directory contains API request collections for testing endpoints.
