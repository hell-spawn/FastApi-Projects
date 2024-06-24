# skypulse

API for getting historical weatcher events

## Development Requirements

- Python3.11.0
- Pip


## Runnning Localhost

`make run`

## Running Tests

`make test`

## Access Swagger Documentation

> <http://localhost:8080/docs>

## Access Redocs Documentation

> <http://localhost:8080/redoc>

## Project structure
    app
    ├── api                 - API related functionaltiy.
    │   └── routes          - Routes for API.
    ├── core                - application configuration, startup events, logging.
    ├── models              - pydantic models for this application.
    ├── schemas             - TODO
    ├── services            - logic that is not just crud related.
    └── main.py             - FastAPI application creation and configuration.
    └── tests            - pytest


# Generate migration
alembic init -t async alembic

# Generate new migration file
alembic revision --autogenerate -m "Add Tutorial model"

# Apply the migration
$ al Tembic upgrade head


