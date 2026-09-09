"""DocuMind Streamlit application entry point."""

import streamlit as st

from app.ui.chat import render_chat_page
from app.ui.home import render_home_page
from app.ui.styles import apply_global_styles, load_image_base64
from app.ui.upload import render_upload_page
from app.utils.logger import setup_logging

logger = setup_logging()

def render_sidebar() -> str:
    """Render the DocuMind navigation sidebar."""

    logo_b64 = load_image_base64("logo.png")

    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <img class="sidebar-brand-logo" src="data:image/png;base64,{logo_b64}" alt="DocuMind Logo" />
                <div class="sidebar-brand-title">DOCUMIND</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-section">Workspace</div>',
            unsafe_allow_html=True,
        )

        if "current_page" not in st.session_state:
            st.session_state.current_page = "Documents"

        with st.container(key="workspace_nav"):
            if st.button(
                "Documents",
                key="workspace_documents",
                type=(
                    "primary"
                    if st.session_state.current_page == "Documents"
                    else "secondary"
                ),
                width="stretch",
            ):
                st.session_state.current_page = "Documents"
                st.rerun()

            if st.button(
                "Ask DocuMind",
                key="workspace_ask",
                type=(
                    "primary"
                    if st.session_state.current_page == "Ask DocuMind"
                    else "secondary"
                ),
                width="stretch",
            ):
                st.session_state.current_page = "Ask DocuMind"
                st.rerun()

            if st.button(
                "Upload",
                key="workspace_upload",
                type=(
                    "primary"
                    if st.session_state.current_page == "Upload"
                    else "secondary"
                ),
                width="stretch",
            ):
                st.session_state.current_page = "Upload"
                st.rerun()

        st.markdown(
            '<div class="sidebar-section sidebar-system-title">System</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """<div class="sidebar-system-status"><div><span class="status-dot"></span>RAG engine ready</div><div>Gemini and MMR</div></div>""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-footer-brand">
                <div class="sidebar-footer-title">DOCUMIND</div>
                <div class="sidebar-footer-subtitle">
                    Document Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.current_page

def main() -> None:
    """Launch the DocuMind application."""

    logger.info("Application started")

    st.set_page_config(
        page_title="DocuMind — Document Intelligence",
        page_icon="static/logo.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_global_styles()
    page = render_sidebar()

    if page == "Documents":
        render_home_page()
    elif page == "Ask DocuMind":
        render_chat_page()
    else:
        render_upload_page()


if __name__ == "__main__":
    main()