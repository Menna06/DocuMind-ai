# ADR-002: AI Orchestration Framework

## Status

Approved

## Decision

LangChain

## Context

The RAG pipeline requires orchestration of document loading, embeddings, retrievers, prompt templates, and chains.

## Alternatives Considered

- LlamaIndex
- Haystack
- Custom implementation

## Rationale

LangChain provides mature abstractions for document loading, embeddings, retrievers, prompt templates, and RAG chains. It is widely recognized and aligns with industry expectations.

## Consequences

- Faster development through proven abstractions
- Easy component replacement in future versions
