# RAG Pipeline Specification

This document describes the Retrieval-Augmented Generation pipeline implemented in DocuMind AI Version 1.0.

## Pipeline Stages

### Stage 1 — Document Upload

- Validate PDF file type
- Store uploaded files in `data/uploads/`
- Trigger automatic indexing

### Stage 2 — Document Loading

- **Component:** LangChain `PyPDFLoader`
- Extract text from every page
- Preserve page ordering and metadata

### Stage 3 — Text Chunking

- **Component:** LangChain `RecursiveCharacterTextSplitter`
- **Chunk Size:** 1000 characters
- **Chunk Overlap:** 200 characters

### Stage 4 — Embedding Generation

- **Component:** OpenAI Embeddings (`text-embedding-3-small`)
- Convert each chunk into a semantic vector

### Stage 5 — Vector Storage

- **Component:** ChromaDB
- Store embeddings with metadata: document name, page number, chunk text

### Stage 6 — Semantic Retrieval

- Embed user query
- Perform similarity search
- Return top-K relevant chunks (default: 5)

### Stage 7 — Prompt Construction

- Combine system instructions, retrieved context, and user question
- Instruct model to answer only from provided context

### Stage 8 — Response Generation

- **Component:** OpenAI Chat Completions API
- Generate grounded answer with source citations

## Citation Strategy

Every response includes:

- Document name
- Page number
- Retrieved passage excerpt

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Missing API key | Display configuration error, do not crash |
| Empty retrieval | Inform user, do not fabricate answer |
| OpenAI API failure | Log exception, display friendly message |
| Corrupted PDF | Reject upload, log issue, continue running |

## Configuration

All pipeline parameters are configurable via environment variables. See `.env.example`.
