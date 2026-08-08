"""Tests for the complete RAG pipeline."""

from unittest.mock import Mock

from langchain_core.documents import Document

import app.rag.pipeline as pipeline_module


def test_retrieve_context_returns_combined_document_text(
    monkeypatch,
) -> None:
    """Retrieved document text should be combined into context."""

    documents = [
        Document(
            page_content="First relevant chunk.",
            metadata={"source": "test.pdf", "page": 0},
        ),
        Document(
            page_content="Second relevant chunk.",
            metadata={"source": "test.pdf", "page": 1},
        ),
    ]

    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = documents

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )

    pipeline = pipeline_module.RAGPipeline()

    result = pipeline.retrieve_context("What is in the document?")

    assert result.context == (
        "First relevant chunk.\n\n"
        "Second relevant chunk."
    )
    assert result.documents == documents

    mock_retriever.retrieve.assert_called_once_with(
        "What is in the document?"
    )


def test_retrieve_context_preserves_document_metadata(
    monkeypatch,
) -> None:
    """Retrieved document metadata should remain available."""

    documents = [
        Document(
            page_content="Relevant content.",
            metadata={
                "source": "legal_document.pdf",
                "page": 3,
            },
        ),
    ]

    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = documents

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )

    pipeline = pipeline_module.RAGPipeline()

    result = pipeline.retrieve_context("Find the relevant section.")

    assert result.documents[0].metadata["source"] == "legal_document.pdf"
    assert result.documents[0].metadata["page"] == 3


def test_empty_query_returns_empty_result(monkeypatch) -> None:
    """An empty query should produce an empty retrieval result."""

    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = []

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )

    pipeline = pipeline_module.RAGPipeline()

    result = pipeline.retrieve_context("")

    assert result.context == ""
    assert result.documents == []

    mock_retriever.retrieve.assert_called_once_with("")


def test_documents_with_empty_content_are_excluded(
    monkeypatch,
) -> None:
    """Documents without text should not add empty content to the context."""

    documents = [
        Document(
            page_content="First chunk.",
            metadata={"source": "test.pdf", "page": 0},
        ),
        Document(
            page_content="   ",
            metadata={"source": "test.pdf", "page": 1},
        ),
        Document(
            page_content="Third chunk.",
            metadata={"source": "test.pdf", "page": 2},
        ),
    ]

    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = documents

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )

    pipeline = pipeline_module.RAGPipeline()

    result = pipeline.retrieve_context("Test query")

    assert result.context == "First chunk.\n\nThird chunk."
    assert result.documents == documents