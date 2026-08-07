"""Tests for application configuration."""

from app.config.settings import get_settings


def test_settings_load_with_defaults() -> None:
    """Settings should load with sensible defaults when env vars are absent."""
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.chunk_size == 1000
    assert settings.chunk_overlap == 200
    assert settings.retrieval_top_k == 5
    assert settings.openai_embedding_model == "text-embedding-3-small"


def test_settings_ensure_directories(tmp_path, monkeypatch) -> None:
    """Settings should create required directories on initialization."""
    get_settings.cache_clear()
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "data" / "uploads"))
    monkeypatch.setenv("VECTORSTORE_DIR", str(tmp_path / "vectorstore"))

    settings = get_settings()
    assert settings.data_dir.exists()
    assert settings.upload_dir.exists()
    assert settings.vectorstore_dir.exists()
