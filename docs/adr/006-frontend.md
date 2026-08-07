# ADR-006: Frontend Framework

## Status

Approved

## Decision

Streamlit

## Context

Version 1.0 requires an interactive web interface for document upload and chat without frontend framework complexity.

## Alternatives Considered

- React + FastAPI
- Gradio
- Flask + Jinja2

## Rationale

Streamlit enables rapid creation of interactive AI applications. Version 1.0 prioritizes AI Engineering demonstration over frontend engineering.

## Consequences

- Single Python codebase for UI and backend logic (with separation of concerns enforced architecturally)
- Future migration to React + FastAPI planned for Version 1.2
