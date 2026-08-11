"""Tests for LLM answer generation."""

from unittest.mock import Mock

import pytest

import app.rag.llm as llm_module


def test_generate_answer_returns_model_response(monkeypatch) -> None:
    """The answer generator should return the model response."""

    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    llm_module.get_settings.cache_clear()

    mock_model = Mock()
    mock_response = Mock()
    mock_response.content = "The project used Java and Spring Boot."
    mock_model.invoke.return_value = mock_response

    monkeypatch.setattr(
        llm_module,
        "ChatGoogleGenerativeAI",
        lambda **kwargs: mock_model,
    )

    generator = llm_module.DocumentAnswerGenerator()

    answer = generator.generate_answer(
        "What technologies were used?",
        "The project used Java and Spring Boot.",
    )

    assert answer == "The project used Java and Spring Boot."

    mock_model.invoke.assert_called_once()


def test_empty_question_returns_empty_answer(monkeypatch) -> None:
    """An empty question should not call the language model."""

    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    llm_module.get_settings.cache_clear()

    mock_model = Mock()

    monkeypatch.setattr(
        llm_module,
        "ChatGoogleGenerativeAI",
        lambda **kwargs: mock_model,
    )

    generator = llm_module.DocumentAnswerGenerator()

    answer = generator.generate_answer(
        "",
        "Some document context.",
    )

    assert answer == ""
    mock_model.invoke.assert_not_called()


def test_empty_context_returns_fallback_answer(monkeypatch) -> None:
    """An empty context should not call the language model."""

    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    llm_module.get_settings.cache_clear()

    mock_model = Mock()

    monkeypatch.setattr(
        llm_module,
        "ChatGoogleGenerativeAI",
        lambda **kwargs: mock_model,
    )

    generator = llm_module.DocumentAnswerGenerator()

    answer = generator.generate_answer(
        "What does the document say?",
        "",
    )

    assert (
        answer
        == "The information is not available in the provided documents."
    )

    mock_model.invoke.assert_not_called()


def test_missing_api_key_is_rejected(monkeypatch) -> None:
    """Answer generation should require a Gemini API key."""

    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_API_KEY", "")
    llm_module.get_settings.cache_clear()

    with pytest.raises(
        ValueError,
        match="GEMINI_API_KEY must be configured",
    ):
        llm_module.DocumentAnswerGenerator()

    llm_module.get_settings.cache_clear()