"""DocuMind Streamlit application entry point."""

import streamlit as st

from app.ui.chat import render_chat_page
from app.ui.home import render_home_page
from app.ui.styles import apply_global_styles
from app.ui.upload import render_upload_page
from app.utils.logger import setup_logging
from app.ui.document_showcase import render_document_showcase

logger = setup_logging()


def render_sidebar() -> str:
    """Render the DocuMind navigation sidebar."""

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-title">DOCUMIND</div>
                <div class="sidebar-brand-subtitle">
                    Document Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section">Workspace</div>',
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Navigation",
            [
                "Documents",
                "Ask DocuMind",
                "Upload",
                "Document System",
            ],
            label_visibility="collapsed",
        )

        st.markdown(
            '<div class="sidebar-section">System</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="
                color:#77717B;
                font-size:0.78rem;
                line-height:1.8;
            ">
                <div>
                    <span class="status-dot"></span>
                    RAG engine ready
                </div>
                <div>Gemini generation</div>
                <div>MMR retrieval</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return page


def main() -> None:
    """Launch the DocuMind application."""

    logger.info("Application started")

    st.set_page_config(
        page_title="DocuMind — Document Intelligence",
        page_icon="D",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_global_styles()
    page = render_sidebar()

    if page == "Documents":
        render_home_page()
    elif page == "Ask DocuMind":
        render_chat_page()
    elif page == "Document System":
        render_document_showcase()
    else:
        render_upload_page()


if __name__ == "__main__":
    main()