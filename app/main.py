"""DocuMind Streamlit application entry point."""

import streamlit as st

from app.ui.home import render_home_page
from app.ui.upload import render_upload_page
from app.utils.logger import setup_logging


logger = setup_logging()


def main() -> None:
    """Launch the DocuMind application."""

    logger.info("Application started")

    st.set_page_config(
        page_title="DocuMind",
        page_icon="D",
        layout="wide",
    )

    st.sidebar.title("DocuMind")

    page = st.sidebar.radio(
        "Navigation",
        ["Documents", "Upload"],
    )

    if page == "Documents":
        render_home_page()
    else:
        render_upload_page()


if __name__ == "__main__":
   """DocuMind Streamlit application entry point."""

import streamlit as st

from app.ui.chat import render_chat_page
from app.ui.home import render_home_page
from app.ui.upload import render_upload_page
from app.utils.logger import setup_logging


logger = setup_logging()


def main() -> None:
    """Launch the DocuMind application."""

    logger.info("Application started")

    st.set_page_config(
        page_title="DocuMind",
        page_icon="D",
        layout="wide",
    )

    st.sidebar.title("DocuMind")

    page = st.sidebar.radio(
        "Navigation",
        ["Documents", "Chat", "Upload"],
    )

    if page == "Documents":
        render_home_page()
    elif page == "Chat":
        render_chat_page()
    else:
        render_upload_page()


if __name__ == "__main__":
    main()