# ADR-010: Deployment Strategy

## Status

Approved

## Decision

Local Development

## Context

Version 1.0 is scoped as a portfolio MVP demonstrating AI Engineering skills.

## Alternatives Considered

- Docker containerization
- Cloud deployment (AWS, GCP, Azure)
- Kubernetes orchestration

## Rationale

Local development keeps the project focused on core AI Engineering concepts while preserving a clean migration path for future versions.

## Consequences

- No Docker, CI/CD, or cloud infrastructure in Version 1.0
- Future releases (1.2+) will add Docker, FastAPI, and enterprise deployment
