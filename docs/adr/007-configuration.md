# ADR-007: Configuration Management

## Status

Approved

## Decision

python-dotenv with environment variables

## Context

API keys and configuration values must never be hardcoded in source code.

## Alternatives Considered

- YAML configuration files
- Pydantic Settings with secrets manager
- Hardcoded defaults

## Rationale

Environment variables loaded from a `.env` file provide a simple, secure, and widely adopted configuration pattern for local development.

## Consequences

- `.env` file must be created from `.env.example` before running
- `.env` is excluded from version control via `.gitignore`
