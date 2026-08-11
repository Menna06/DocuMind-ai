"""Application settings loaded from environment variables."""

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass(frozen=True)
class Settings:
    """Central configuration for DocuMind AI."""

    llm_provider: str
    embedding_provider: str

    gemini_api_key: str
    gemini_embedding_model: str
    gemini_chat_model: str

    openai_api_key: str
    openai_embedding_model: str
    openai_chat_model: str

    chunk_size: int
    chunk_overlap: int
    retrieval_top_k: int
    data_dir: Path
    upload_dir: Path
    vectorstore_dir: Path
    log_level: str

    @property
    def is_configured(self) -> bool:
        """Return True when the selected AI provider is configured."""

        if self.llm_provider == "gemini":
            return bool(self.gemini_api_key.strip())

        if self.llm_provider == "openai":
            return bool(self.openai_api_key.strip())

        return False

    def ensure_directories(self) -> None:
        """Create required application directories if they do not exist."""

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.vectorstore_dir.mkdir(parents=True, exist_ok=True)


def _parse_int(value: str | None, default: int) -> int:
    if value is None or not value.strip():
        return default

    return int(value)


def _parse_path(value: str | None, default: Path) -> Path:
    if value is None or not value.strip():
        return default

    path = Path(value)

    return path if path.is_absolute() else PROJECT_ROOT / path


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""

    settings = Settings(
        llm_provider=os.getenv("LLM_PROVIDER", "gemini"),
        embedding_provider=os.getenv(
            "EMBEDDING_PROVIDER",
            "gemini",
        ),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_embedding_model=os.getenv(
            "GEMINI_EMBEDDING_MODEL",
            "gemini-embedding-001",
        ),
        gemini_chat_model=os.getenv(
            "GEMINI_CHAT_MODEL",
            "gemini-2.5-flash",
        ),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_embedding_model=os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            "text-embedding-3-small",
        ),
        openai_chat_model=os.getenv(
            "OPENAI_CHAT_MODEL",
            "gpt-4.1",
        ),
        chunk_size=_parse_int(
            os.getenv("CHUNK_SIZE"),
            1000,
        ),
        chunk_overlap=_parse_int(
            os.getenv("CHUNK_OVERLAP"),
            200,
        ),
        retrieval_top_k=_parse_int(
            os.getenv("RETRIEVAL_TOP_K"),
            5,
        ),
        data_dir=_parse_path(
            os.getenv("DATA_DIR"),
            PROJECT_ROOT / "data",
        ),
        upload_dir=_parse_path(
            os.getenv("UPLOAD_DIR"),
            PROJECT_ROOT / "data" / "uploads",
        ),
        vectorstore_dir=_parse_path(
            os.getenv("VECTORSTORE_DIR"),
            PROJECT_ROOT / "vectorstore",
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )

    settings.ensure_directories()

    return settings