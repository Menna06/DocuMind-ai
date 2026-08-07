# DocuMind AI

Enterprise intelligent document search and question-answering platform powered by Retrieval-Augmented Generation (RAG).

DocuMind AI enables users to upload PDF documents, automatically index their contents using semantic embeddings, and interact with those documents through natural language conversations grounded in retrieved context.

## Features (Version 1.0)

- **Document Upload** — Upload one or more PDF documents through a Streamlit web interface
- **Document Processing** — Automatic ingestion pipeline: load, extract, chunk, embed, and store
- **Semantic Search** — Retrieve relevant passages using vector similarity rather than keyword matching
- **Question Answering** — Ask natural language questions and receive grounded responses
- **Document Summarization** — Generate concise summaries from uploaded documents
- **Source Citations** — Every answer includes traceable document sources with page references

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| UI | Streamlit |
| Orchestration | LangChain |
| Vector Database | ChromaDB |
| Embeddings | OpenAI Embeddings |
| LLM | OpenAI Chat Completions API |
| Configuration | python-dotenv |
| Testing | pytest |
| Formatting | Black |
| Linting | Ruff |

## Project Structure

```
documind-ai/
├── app/
│   ├── config/          # Application settings and environment configuration
│   ├── rag/             # RAG pipeline: loader, chunker, embeddings, retrieval
│   ├── services/        # Business workflow coordination
│   ├── prompts/         # Prompt templates
│   ├── ui/              # Streamlit interface pages
│   ├── utils/           # Logging and shared utilities
│   └── main.py          # Application entry point
├── tests/               # Automated test suite
├── docs/                # Architecture and design documentation
├── data/                # Uploaded documents (local storage)
├── vectorstore/         # ChromaDB persistence directory
├── assets/              # Static assets
└── .github/             # GitHub templates and workflows
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- OpenAI API key

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd DocuMind-ai
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   ```bash
   cp .env.example .env
   # Edit .env and set your OPENAI_API_KEY
   ```

### Running the Application

```bash
streamlit run app/main.py
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black app/ tests/
ruff check app/ tests/
```

## Architecture

DocuMind AI follows a modular layered architecture:

```
Streamlit UI → Application Services → RAG Pipeline → Grounded Response + Citations
```

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation and [docs/adr/](docs/adr/) for Architecture Decision Records.

## Development Workflow

This project is developed incrementally using feature branches. Each engineering ticket produces production-quality, tested code before moving to the next capability.

## License

This project is developed as an AI Engineering portfolio demonstration.
