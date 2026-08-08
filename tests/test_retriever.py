"""Tests for semantic retrieval."""

from unittest.mock import Mock

from langchain_core.documents import Document

import app.rag.retriever as retriever_module


def test_retrieve_returns_relevant_documents(monkeypatch) -> None:
    """A query should return documents from the vector store."""

    expected_documents = [
        Document(
            page_content="First relevant chunk.",
            metadata={"source": "test.pdf", "page": 0},
        ),
        Document(
            page_content="Second relevant chunk.",
            metadata={"source": "test.pdf", "page": 1},
        ),
    ]

    mock_vector_store = Mock()
    mock_vector_store.store.similarity_search.return_value = (
        expected_documents
    )

    monkeypatch.setattr(
        retriever_module,
        "DocumentVectorStore",
        lambda: mock_vector_store,
    )
    monkeypatch.setattr(
        retriever_module,
        "get_settings",
        lambda: Mock(retrieval_top_k=5),
    )

    retriever = retriever_module.DocumentRetriever()

    documents = retriever.retrieve("What is in the document?")

    assert documents == expected_documents

    mock_vector_store.store.similarity_search.assert_called_once_with(
        "What is in the document?",
        k=5,
    )


def test_retrieve_uses_custom_top_k(monkeypatch) -> None:
    """A custom result limit should be passed to the vector store."""

    mock_vector_store = Mock()
    mock_vector_store.store.similarity_search.return_value = []

    monkeypatch.setattr(
        retriever_module,
        "DocumentVectorStore",
        lambda: mock_vector_store,
    )
    monkeypatch.setattr(
        retriever_module,
        "get_settings",
        lambda: Mock(retrieval_top_k=5),
    )

    retriever = retriever_module.DocumentRetriever()

    result = retriever.retrieve("Test query", top_k=3)

    assert result == []

    mock_vector_store.store.similarity_search.assert_called_once_with(
        "Test query",
        k=3,
    )


def test_empty_query_returns_no_documents(monkeypatch) -> None:
    """An empty query should not perform a vector store search."""

    mock_vector_store = Mock()

    monkeypatch.setattr(
        retriever_module,
        "DocumentVectorStore",
        lambda: mock_vector_store,
    )
    monkeypatch.setattr(
        retriever_module,
        "get_settings",
        lambda: Mock(retrieval_top_k=5),
    )

    retriever = retriever_module.DocumentRetriever()

    assert retriever.retrieve("   ") == []

    mock_vector_store.store.similarity_search.assert_not_called()


def test_non_positive_top_k_returns_no_documents(monkeypatch) -> None:
    """A non-positive result limit should not perform a search."""

    mock_vector_store = Mock()

    monkeypatch.setattr(
        retriever_module,
        "DocumentVectorStore",
        lambda: mock_vector_store,
    )
    monkeypatch.setattr(
        retriever_module,
        "get_settings",
        lambda: Mock(retrieval_top_k=5),
    )

    retriever = retriever_module.DocumentRetriever()

    assert retriever.retrieve("Test query", top_k=0) == []

    mock_vector_store.store.similarity_search.assert_not_called()
