"""Tests for embedding generation."""

from unittest.mock import Mock

import pytest
from langchain_core.documents import Document

import app.rag.embeddings as embeddings_module
from app.rag.embeddings import DocumentEmbedder


def test_embed_documents_returns_embeddings(monkeypatch) -> None:
    """Document chunks should be converted into embedding vectors."""

    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    embeddings_module.get_settings.cache_clear()

    mock_embeddings = Mock()
    mock_embeddings.embed_documents.return_value = [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    monkeypatch.setattr(
        embeddings_module,
        "GoogleGenerativeAIEmbeddings",
        lambda **kwargs: mock_embeddings,
    )

    documents = [
        Document(
            page_content="First document chunk.",
            metadata={"source": "test.pdf", "page": 0},
        ),
        Document(
            page_content="Second document chunk.",
            metadata={"source": "test.pdf", "page": 1},
        ),
    ]

    embedder = DocumentEmbedder()
    embeddings = embedder.embed_documents(documents)

    assert embeddings == [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
    ]

    mock_embeddings.embed_documents.assert_called_once_with(
        [
            "First document chunk.",
            "Second document chunk.",
        ]
    )


def test_empty_document_list_returns_no_embeddings(
    monkeypatch,
) -> None:
    """An empty document list should return an empty result."""

    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    embeddings_module.get_settings.cache_clear()

    mock_embeddings = Mock()

    monkeypatch.setattr(
        embeddings_module,
        "GoogleGenerativeAIEmbeddings",
        lambda **kwargs: mock_embeddings,
    )

    embedder = DocumentEmbedder()

    assert embedder.embed_documents([]) == []

    mock_embeddings.embed_documents.assert_not_called()


def test_missing_gemini_api_key_is_rejected(monkeypatch) -> None:
    """Gemini embeddings should require a Gemini API key."""

    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "")

    embeddings_module.get_settings.cache_clear()

    with pytest.raises(
        ValueError,
        match="GEMINI_API_KEY must be configured",
    ):
        DocumentEmbedder()

    embeddings_module.get_settings.cache_clear()