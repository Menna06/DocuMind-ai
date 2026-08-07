# ADR-008: Logging

## Status

Approved

## Decision

Python standard library `logging` module

## Context

Application events must be logged for debugging without exposing sensitive information.

## Alternatives Considered

- structlog
- loguru
- Custom logging wrapper

## Rationale

The standard library provides sufficient functionality while avoiding unnecessary dependencies. Sensitive information such as API keys must never be written to logs.

## Consequences

- Logging configured centrally in `app/utils/logging.py`
- Log level configurable via `LOG_LEVEL` environment variable
