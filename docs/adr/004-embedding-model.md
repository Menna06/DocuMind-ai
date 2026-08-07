# ADR-004: Embedding Model

## Status

Approved

## Decision

OpenAI Embeddings (`text-embedding-3-small`)

## Context

Document chunks must be converted to semantic vectors for similarity search.

## Alternatives Considered

- SentenceTransformers
- HuggingFace
- Voyage AI
- Gemini Embeddings

## Rationale

OpenAI embeddings provide high-quality semantic representations with excellent LangChain integration. API-based inference allows efficient operation on modest hardware.

## Consequences

- Requires OpenAI API key and network access
- No local GPU required for embedding generation
