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


def test_delete_document_removes_matching_chunks(monkeypatch, tmp_path) -> None:
    """Deleting a document should delete only chunks belonging to that filename."""

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    vectorstore_module.get_settings.cache_clear()

    mock_collection = Mock()
    mock_collection.get.return_value = {
        "ids": ["id-1", "id-2", "id-3", "id-4"],
        "metadatas": [
            {"source": "data/uploads/target.pdf", "page": 0},
            {"source": "data/uploads/other.pdf", "page": 0},
            {"source": "/var/app/data/uploads/target.pdf", "page": 1},
            {"source": "target.pdf", "page": 2},
        ],
    }

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
    deleted_count = store.delete_document("target.pdf")

    assert deleted_count == 3
    mock_store.delete.assert_called_once_with(ids=["id-1", "id-3", "id-4"])


def test_delete_document_nonexistent_returns_zero(monkeypatch, tmp_path) -> None:
    """Deleting a document not present in vector store returns zero and does not delete."""

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    vectorstore_module.get_settings.cache_clear()

    mock_collection = Mock()
    mock_collection.get.return_value = {
        "ids": ["id-1"],
        "metadatas": [{"source": "data/uploads/other.pdf", "page": 0}],
    }

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
    deleted_count = store.delete_document("missing.pdf")

    assert deleted_count == 0
    mock_store.delete.assert_not_called()


def test_delete_document_empty_or_none_returns_zero(monkeypatch, tmp_path) -> None:
    """Deleting with empty filename returns zero without querying collection."""

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    vectorstore_module.get_settings.cache_clear()

    mock_collection = Mock()
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
    assert store.delete_document("") == 0
    mock_collection.get.assert_not_called()
    mock_store.delete.assert_not_called()


def test_vector_store_delete_document_real_chroma(tmp_path, monkeypatch) -> None:
    """Integration test with real Chroma store demonstrating chunk deletion and isolation."""

    class DeterministicFakeEmbeddings:
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [[0.1] * 8 for _ in texts]

        def embed_query(self, text: str) -> list[float]:
            return [0.1] * 8

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    vectorstore_module.get_settings.cache_clear()

    mock_embedder = Mock()
    mock_embedder.embeddings = DeterministicFakeEmbeddings()

    monkeypatch.setattr(
        vectorstore_module,
        "DocumentEmbedder",
        lambda: mock_embedder,
    )
    monkeypatch.setattr(
        vectorstore_module,
        "get_settings",
        lambda: Mock(vectorstore_dir=tmp_path),
    )

    store = vectorstore_module.DocumentVectorStore()

    # Add chunks for two different documents (TC-10 isolation verification)
    doc_a_chunks = [
        Document(page_content="A1", metadata={"source": "data/uploads/doc_a.pdf", "page": 0}),
        Document(page_content="A2", metadata={"source": "data/uploads/doc_a.pdf", "page": 1}),
    ]
    doc_b_chunks = [
        Document(page_content="B1", metadata={"source": "data/uploads/doc_b.pdf", "page": 0}),
    ]

    store.add_documents(doc_a_chunks + doc_b_chunks)
    assert store.count() == 3

    # Delete doc_a (TC-09)
    deleted = store.delete_document("doc_a.pdf")
    assert deleted == 2

    # doc_a chunks are gone, doc_b remains intact (TC-10)
    assert store.count() == 1

    remaining_data = store.store._collection.get(include=["metadatas"])
    remaining_sources = [m["source"] for m in remaining_data["metadatas"]]
    assert remaining_sources == ["data/uploads/doc_b.pdf"]