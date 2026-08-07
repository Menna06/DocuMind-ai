# ADR-009: Code Quality

## Status

Approved

## Decision

Black (formatting), Ruff (linting), pytest (testing)

## Context

The project must demonstrate professional development practices comparable to production engineering teams.

## Alternatives Considered

- flake8 + isort
- pylint
- no automated tooling

## Rationale

These tools are lightweight, widely adopted, and easy to integrate into continuous integration in future releases.

## Consequences

- Code formatting enforced via Black
- Lint rules configured in `pyproject.toml`
- Test suite runnable via `pytest`
