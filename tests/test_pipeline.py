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

    mock_answer_generator = Mock()

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )
    monkeypatch.setattr(
        pipeline_module,
        "DocumentAnswerGenerator",
        lambda: mock_answer_generator,
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

    mock_answer_generator = Mock()

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )
    monkeypatch.setattr(
        pipeline_module,
        "DocumentAnswerGenerator",
        lambda: mock_answer_generator,
    )

    pipeline = pipeline_module.RAGPipeline()

    result = pipeline.retrieve_context("Find the relevant section.")

    assert result.documents[0].metadata["source"] == "legal_document.pdf"
    assert result.documents[0].metadata["page"] == 3


def test_empty_query_returns_empty_result(monkeypatch) -> None:
    """An empty query should produce an empty retrieval result."""

    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = []

    mock_answer_generator = Mock()

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )
    monkeypatch.setattr(
        pipeline_module,
        "DocumentAnswerGenerator",
        lambda: mock_answer_generator,
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

    mock_answer_generator = Mock()

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )
    monkeypatch.setattr(
        pipeline_module,
        "DocumentAnswerGenerator",
        lambda: mock_answer_generator,
    )

    pipeline = pipeline_module.RAGPipeline()

    result = pipeline.retrieve_context("Test query")

    assert result.context == "First chunk.\n\nThird chunk."
    assert result.documents == documents


def test_query_returns_generated_answer_and_documents(
    monkeypatch,
) -> None:
    """A query should return the generated answer and supporting documents."""

    documents = [
        Document(
            page_content="The project used Java and Spring Boot.",
            metadata={"source": "project.pdf", "page": 0},
        ),
        Document(
            page_content="The application used PostgreSQL.",
            metadata={"source": "project.pdf", "page": 1},
        ),
    ]

    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = documents

    mock_answer_generator = Mock()
    mock_answer_generator.generate_answer.return_value = (
        "The project used Java, Spring Boot, and PostgreSQL."
    )

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )
    monkeypatch.setattr(
        pipeline_module,
        "DocumentAnswerGenerator",
        lambda: mock_answer_generator,
    )

    pipeline = pipeline_module.RAGPipeline()

    result = pipeline.query("What technologies were used?")

    assert result.answer == (
        "The project used Java, Spring Boot, and PostgreSQL."
    )
    assert result.context == (
        "The project used Java and Spring Boot.\n\n"
        "The application used PostgreSQL."
    )
    assert result.documents == documents

    mock_retriever.retrieve.assert_called_once_with(
        "What technologies were used?"
    )

    mock_answer_generator.generate_answer.assert_called_once_with(
        "What technologies were used?",
        (
            "The project used Java and Spring Boot.\n\n"
            "The application used PostgreSQL."
        ),
    )


def test_query_with_no_retrieved_documents_returns_empty_context(
    monkeypatch,
) -> None:
    """A query without retrieved documents should preserve an empty context."""

    mock_retriever = Mock()
    mock_retriever.retrieve.return_value = []

    mock_answer_generator = Mock()
    mock_answer_generator.generate_answer.return_value = (
        "The information is not available in the provided documents."
    )

    monkeypatch.setattr(
        pipeline_module,
        "DocumentRetriever",
        lambda: mock_retriever,
    )
    monkeypatch.setattr(
        pipeline_module,
        "DocumentAnswerGenerator",
        lambda: mock_answer_generator,
    )

    pipeline = pipeline_module.RAGPipeline()

    result = pipeline.query("What does the document say?")

    assert result.answer == (
        "The information is not available in the provided documents."
    )
    assert result.context == ""
    assert result.documents == []

    mock_answer_generator.generate_answer.assert_called_once_with(
        "What does the document say?",
        "",
    )