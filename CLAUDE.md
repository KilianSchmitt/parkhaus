# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Parkhaus is a Python-based REST API built with FastAPI, featuring GraphQL support via Strawberry, PostgreSQL database with SQLAlchemy ORM, and Keycloak for authentication. It's a university project demonstrating modern Python web development patterns.

## Development Commands

### Dependency Management

- `uv sync --all-groups` - Install all dependencies including dev and doc groups
- `uv tree --outdated` - Check for outdated packages

### Running the Application

- `uv run parkhaus` - Run the application using the package entry point
- `uv run python -m parkhaus` - Run as a module
- `uv run fastapi dev src/parkhaus` - Run with FastAPI dev server (hot reload)
- `uv run uvicorn src.parkhaus:app --ssl-certfile=src/parkhaus/config/resources/tls/certificate.crt --ssl-keyfile=src/parkhaus/config/resources/tls/key.pem` - Run with TLS

### Testing

- `uv run pytest` - Run all tests
- `uv run pytest -m rest` - Run only REST tests (markers defined in pyproject.toml)
- `uv run pytest -k test_post_invalid_json` - Run specific test by name

### Code Quality

- `uvx ruff check src tests` - Lint all code
- `uvx ruff check --fix src tests` - Auto-fix linting issues
- `uvx ruff format src tests` - Format all code
- `uvx ruff format --check src tests` - Check formatting without changes
- `uvx ty check src tests` - Type check with Astral's Ty

### Documentation

- `uv run mkdocs serve` - Serve documentation locally

### Load Testing

- `uvx locust -f ./extras/locustfile.py` - Run load tests with Locust

## Architecture Overview

### Domain Model

The application models a parking garage (**Parkhaus**) as the aggregate root:

- **Parkhaus** (Aggregate Root) → has one **Adresse** (1:1 relationship)
- **Parkhaus** → has many **Auto** (1:N relationship)

**Kundentyp** is an enum (PREMIUM, BASIS, ANWOHNER) decorated with `@strawberry.enum` for GraphQL support.

### Directory Structure

```
src/parkhaus/
├── config/           # Configuration management
│   ├── resources/    # app.toml, TLS certs, SQL scripts
│   ├── dev/          # Database and Keycloak population for dev mode
│   └── *.py          # Modular config (db, keycloak, tls, etc.)
├── entity/           # SQLAlchemy ORM entities
│   ├── base.py       # DeclarativeBase with MappedAsDataclass
│   ├── parhaus.py, adresse.py, auto.py, kundentyp.py
└── main.py           # FastAPI application entry point
```

### Configuration System

Configuration is loaded from `src/parkhaus/config/resources/app.toml` using `importlib.resources`. The `parkhaus.config.config` module provides:

- `app_config`: Dictionary of all TOML configuration
- `resources_path`: Path string for accessing resources

Configuration modules expose typed constants (e.g., `db_url`, `keycloak_config`).

### Development Mode Features

The application supports a dev mode controlled by `app.toml`:

- `dev.db-populate`: Reload database with test data on startup
- `dev.keycloak-populate`: Populate Keycloak with test users

When enabled, SQL scripts from `config/resources/postgresql/` are executed (drop.sql, create.sql), followed by CSV data loading via PostgreSQL's COPY command.

### Database Layer

- **ORM**: SQLAlchemy 2.0 with mapped columns using `Mapped[T]` typing
- **Driver**: psycopg3 with binary support
- **Migrations**: SQL scripts (not Alembic currently)
- **Base Class**: `DeclarativeBase` mixed with `MappedAsDataclass` for dataclass-style entities
- **Identity Columns**: All entities use SQL Server-style `Identity(start=1000)` for primary keys

### Security Features

- **Authentication**: Keycloak with OAuth2/OIDC via `python-keycloak`
- **TLS**: Full TLS verification for PostgreSQL with CA certificates
- **Password Hashing**: Argon2 (Keycloak default)

### Key Dependencies

- **FastAPI**: Web framework with automatic OpenAPI generation
- **SQLAlchemy**: ORM with dataclass-mapped entities
- **Strawberry**: GraphQL schema definitions and resolvers
- **Pydantic**: Data validation and settings management
- **python-keycloak**: Keycloak integration
- **Loguru**: Structured logging
- **uv**: Modern Python package manager (replaces pip)
- **ruff**: Linting and formatting
- **ty**: Type checking (Astral's modern alternative to mypy/pyright)

### Code Style

- Uses `Final` from `typing` for module-level constants
- Uses `Mapped[T]` for SQLAlchemy columns with type annotations
- German naming for domain concepts (`kennzeichen`, `einfahrtszeit`, `kundentyp`)
- Class-level docstrings with `"""` and attribute descriptions
- Ruff linting with extensive rule set including FastAPI, async, and security rules

### Testing Markers

Tests are organized with markers defined in `pyproject.toml`:
- `rest`, `graphql`: Interface types
- `get_request`, `post_request`, `put_request`, `delete_request`: HTTP verbs
- `unit`: Unit tests
- `simple`: Basic boolean tests
