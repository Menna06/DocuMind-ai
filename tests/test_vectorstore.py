"""Tests for ChromaDB vector store management."""

from unittest.mock import Mock

from langchain_core.documents import Document

import app.rag.vectorstore as vectorstore_module


def test_empty_documents_are_not_added(monkeypatch, tmp_path) -> None:
    """An empty document list should not be added to the vector store."""

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    vectorstore_module.get_settings.cache_clear()

    mock_store = Mock()
    mock_embedder = Mock()
    mock_embedder.embeddings = Mock()

    monkeypatch.setattr(
        vectorstore_module,
        "DocumentEmbedder",
        lambda: mock_embedder,
    )
    monkeypatch.setattr(
        vectorstore_module,
        "Chroma",
        lambda **kwargs: mock_store,
    )

    monkeypatch.setattr(
        vectorstore_module,
        "get_settings",
        lambda: Mock(vectorstore_dir=tmp_path),
    )

    store = vectorstore_module.DocumentVectorStore()

    result = store.add_documents([])

    assert result == []
    mock_store.add_documents.assert_not_called()


def test_documents_are_added_to_vector_store(monkeypatch, tmp_path) -> None:
    """Document chunks should be added to the vector store."""

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    vectorstore_module.get_settings.cache_clear()

    mock_store = Mock()
    mock_store.add_documents.return_value = ["id-1", "id-2"]

    mock_embedder = Mock()
    mock_embedder.embeddings = Mock()

    monkeypatch.setattr(
        vectorstore_module,
        "DocumentEmbedder",
        lambda: mock_embedder,
    )
    monkeypatch.setattr(
        vectorstore_module,
        "Chroma",
        lambda **kwargs: mock_store,
    )

    monkeypatch.setattr(
        vectorstore_module,
        "get_settings",
        lambda: Mock(vectorstore_dir=tmp_path),
    )

    documents = [
        Document(
            page_content="First chunk.",
            metadata={"source": "test.pdf", "page": 0},
        ),
        Document(
            page_content="Second chunk.",
            metadata={"source": "test.pdf", "page": 1},
        ),
    ]

    store = vectorstore_module.DocumentVectorStore()
    result = store.add_documents(documents)

    assert result == ["id-1", "id-2"]
    mock_store.add_documents.assert_called_once_with(documents)


def test_vector_store_count_returns_collection_count(
    monkeypatch,
    tmp_path,
) -> None:
    """The vector store should report its current document count."""

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    vectorstore_module.get_settings.cache_clear()

    mock_collection = Mock()
    mock_collection.count.return_value = 4

    mock_store = Mock()
    mock_store._collection = mock_collection

    mock_embedder = Mock()
    mock_embedder.embeddings = Mock()

    monkeypatch.setattr(
        vectorstore_module,
        "DocumentEmbedder",
        lambda: mock_embedder,
    )
    monkeypatch.setattr(
        vectorstore_module,
        "Chroma",
        lambda **kwargs: mock_store,
    )

    monkeypatch.setattr(
        vectorstore_module,
        "get_settings",
        lambda: Mock(vectorstore_dir=tmp_path),
    )

    store = vectorstore_module.DocumentVectorStore()

    assert store.count() == 4