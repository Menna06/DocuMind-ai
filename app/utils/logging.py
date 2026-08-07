"""Application logging configuration."""

import logging
import sys

from app.config.settings import get_settings


def setup_logging() -> logging.Logger:
    """Configure and return the application root logger."""
    settings = get_settings()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    logger = logging.getLogger("documind")
    logger.setLevel(log_level)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger under the documind hierarchy."""
    return logging.getLogger(f"documind.{name}")
