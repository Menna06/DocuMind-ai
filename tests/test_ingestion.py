"""Tests for the document ingestion pipeline."""

from unittest.mock import Mock

from langchain_core.documents import Document

import app.rag.ingestion as ingestion_module


def test_ingest_document_extracts_chunks_and_indexes_them(
    monkeypatch,
) -> None:
    """A document should be extracted, chunked, and added to the vector store."""

    pages = [
        Document(
            page_content="First page content.",
            metadata={"source": "test.pdf", "page": 0},
        ),
        Document(
            page_content="Second page content.",
            metadata={"source": "test.pdf", "page": 1},
        ),
    ]

    chunks = [
        Document(
            page_content="First chunk.",
            metadata={"source": "test.pdf", "page": 0},
        ),
        Document(
            page_content="Second chunk.",
            metadata={"source": "test.pdf", "page": 1},
        ),
    ]

    mock_document_service = Mock()
    mock_document_service.extract_document.return_value = pages

    mock_chunker = Mock()
    mock_chunker.split_documents.return_value = chunks

    mock_vector_store = Mock()
    mock_vector_store.add_documents.return_value = [
        "id-1",
        "id-2",
    ]

    monkeypatch.setattr(
        ingestion_module,
        "DocumentService",
        lambda: mock_document_service,
    )
    monkeypatch.setattr(
        ingestion_module,
        "DocumentChunker",
        lambda: mock_chunker,
    )
    monkeypatch.setattr(
        ingestion_module,
        "DocumentVectorStore",
        lambda: mock_vector_store,
    )

    service = ingestion_module.DocumentIngestionService()

    result = service.ingest_document("test.pdf")

    assert result.filename == "test.pdf"
    assert result.pages == 2
    assert result.chunks == 2
    assert result.document_ids == ["id-1", "id-2"]

    mock_document_service.extract_document.assert_called_once_with(
        "test.pdf"
    )
    mock_chunker.split_documents.assert_called_once_with(pages)
    mock_vector_store.add_documents.assert_called_once_with(chunks)


def test_ingest_document_with_no_pages_returns_empty_result(
    monkeypatch,
) -> None:
    """A document with no extracted pages should not be indexed."""

    mock_document_service = Mock()
    mock_document_service.extract_document.return_value = []

    mock_chunker = Mock()
    mock_vector_store = Mock()

    monkeypatch.setattr(
        ingestion_module,
        "DocumentService",
        lambda: mock_document_service,
    )
    monkeypatch.setattr(
        ingestion_module,
        "DocumentChunker",
        lambda: mock_chunker,
    )
    monkeypatch.setattr(
        ingestion_module,
        "DocumentVectorStore",
        lambda: mock_vector_store,
    )

    service = ingestion_module.DocumentIngestionService()

    result = service.ingest_document("empty.pdf")

    assert result.filename == "empty.pdf"
    assert result.pages == 0
    assert result.chunks == 0
    assert result.document_ids == []

    mock_chunker.split_documents.assert_not_called()
    mock_vector_store.add_documents.assert_not_called()


def test_ingest_document_with_no_chunks_returns_empty_result(
    monkeypatch,
) -> None:
    """A document with no generated chunks should not be indexed."""

    pages = [
        Document(
            page_content="Page content.",
            metadata={"source": "test.pdf", "page": 0},
        ),
    ]

    mock_document_service = Mock()
    mock_document_service.extract_document.return_value = pages

    mock_chunker = Mock()
    mock_chunker.split_documents.return_value = []

    mock_vector_store = Mock()

    monkeypatch.setattr(
        ingestion_module,
        "DocumentService",
        lambda: mock_document_service,
    )
    monkeypatch.setattr(
        ingestion_module,
        "DocumentChunker",
        lambda: mock_chunker,
    )
    monkeypatch.setattr(
        ingestion_module,
        "DocumentVectorStore",
        lambda: mock_vector_store,
    )

    service = ingestion_module.DocumentIngestionService()

    result = service.ingest_document("test.pdf")

    assert result.filename == "test.pdf"
    assert result.pages == 1
    assert result.chunks == 0
    assert result.document_ids == []

    mock_vector_store.add_documents.assert_not_called()