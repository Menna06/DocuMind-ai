# Architecture Overview

DocuMind AI follows a modular layered architecture designed for maintainability, testability, and future extensibility.

## High-Level Architecture

```
                    Streamlit User Interface
                               │
                               ▼
                    Application Service Layer
        ┌────────────────────────────────────────┐
        │ Upload Service                         │
        │ Chat Service                           │
        │ Retrieval Service                      │
        │ Prompt Service                         │
        └────────────────────────────────────────┘
                               │
                               ▼
                       RAG Orchestration Layer
        ┌────────────────────────────────────────┐
        │ Document Loader                        │
        │ Text Chunker                           │
        │ Embedding Generator                    │
        │ Chroma Vector Store                    │
        │ Retriever                              │
        │ Prompt Builder                         │
        │ LLM Client                             │
        └────────────────────────────────────────┘
                               │
                               ▼
                  Grounded Response + Citations
```

## Module Responsibilities

### `app/config/`

Application settings, environment variables, and API configuration. Contains no business logic.

### `app/rag/`

The AI engine implementing the complete RAG pipeline:

| Module | Responsibility |
|--------|----------------|
| `loader.py` | PDF text extraction via PyPDFLoader |
| `chunker.py` | Text splitting via RecursiveCharacterTextSplitter |
| `embeddings.py` | OpenAI embedding generation |
| `vectorstore.py` | ChromaDB persistence and management |
| `retriever.py` | Semantic similarity search |
| `citations.py` | Source citation formatting |
| `pipeline.py` | End-to-end ingestion and query orchestration |

### `app/services/`

Application workflow coordination:

| Module | Responsibility |
|--------|----------------|
| `document_service.py` | Upload validation, storage, and ingestion |
| `chat_service.py` | Question answering and summarization |

### `app/prompts/`

Prompt templates only. No API calls or business logic.

### `app/ui/`

Streamlit pages responsible for rendering, user input, and result display. Contains no RAG logic.

### `app/utils/`

Shared utilities including logging configuration.

## RAG Pipeline Workflow

```
User Uploads PDF
       │
       ▼
Document Processing (Load → Chunk → Embed → Store)
       │
       ▼
User asks Question
       │
       ▼
Query Embedding → Similarity Search → Top-K Retrieval
       │
       ▼
Prompt Construction → LLM Generation → Answer + Citations
```

## Design Principles

- **Single Responsibility** — Each module performs one well-defined task
- **Separation of Concerns** — UI, business logic, and AI pipeline are independent
- **Loose Coupling** — Components communicate through defined interfaces
- **Grounded Generation** — Answers originate from retrieved documents, never model memory alone
- **Explainability** — Every response is traceable to source documents

## Future Migration Path

The architecture supports future expansion without major redesign:

- Vector store: ChromaDB → Pinecone, Weaviate, Azure AI Search
- Frontend: Streamlit → React + FastAPI
- Storage: Local files → PostgreSQL metadata
- Search: Semantic only → Hybrid (Semantic + BM25) with reranking

See [adr/](adr/) for detailed decision records.
