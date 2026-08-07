# ADR-003: Vector Database

## Status

Approved

## Decision

ChromaDB

## Context

Version 1.0 requires a lightweight local vector database without cloud infrastructure dependencies.

## Alternatives Considered

- Pinecone
- Weaviate
- Azure AI Search
- Qdrant

## Rationale

ChromaDB satisfies local development requirements while supporting future migration to enterprise vector databases.

## Consequences

- No cloud infrastructure required for Version 1.0
- Clean migration path to Pinecone, Weaviate, or Azure AI Search in future releases
