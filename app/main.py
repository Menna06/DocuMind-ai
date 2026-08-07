"""DocuMind AI Streamlit application entry point."""

import streamlit as st

from app import __version__
from app.utils.logging import setup_logging

logger = setup_logging()


def main() -> None:
    """Launch the DocuMind AI Streamlit application."""
    logger.info("Application started")
    st.set_page_config(
        page_title="DocuMind AI",
        page_icon="📄",
        layout="wide",
    )
    st.title("DocuMind AI")
    st.caption(f"Version {__version__}")
    st.info(
        "Project skeleton initialized. Application features will be implemented "
        "in subsequent engineering tickets."
    )


if __name__ == "__main__":
    main()
