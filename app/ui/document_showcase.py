"""Temporary QA showcase for the DocuMind Document System."""

import streamlit as st

from app.ui.components import (
    render_document_card,
    render_document_tile,
)


def render_document_showcase() -> None:
    """Render the temporary UI-06 document-system showcase."""

    st.title("UI-06 · Document System")
    st.write(
        "Temporary design-system QA page for the approved "
        "DocuMind document components."
    )

    st.markdown("### 01 · Document Card")

    st.caption(
        "Ready document state with metadata, status badges, "
        "View Text, and Delete actions."
    )

    render_document_card(
        filename="DocuMind_Legal_RAG_Test_Case.pdf",
        pages=2,
        file_size="6.98 KB",
        uploaded_at="2026-08-12 23:40",
        status="ready",
        key="showcase-ready-document",
    )

    st.markdown("### 02 · Processing State")

    st.caption(
        "Same document card while the document is being processed."
    )

    render_document_card(
        filename="DocuMind_Legal_RAG_Test_Case.pdf",
        pages=2,
        file_size="6.98 KB",
        uploaded_at="2026-08-12 23:40",
        status="processing",
        key="showcase-processing-document",
    )

    st.markdown("### 03 · Empty Document Tile")

    st.caption(
        "Reusable structural tile. Content is intentionally "
        "provided later by the page that composes it."
    )

    render_document_tile(
        key="showcase-document-tile",
    )


if __name__ == "__main__":
    render_document_showcase()