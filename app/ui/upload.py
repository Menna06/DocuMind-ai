"""Document upload page rendering."""

import streamlit as st

from app.rag.ingestion import DocumentIngestionService
from app.services.document_service import DocumentService


def render_upload_page() -> None:
    """Render the document upload and ingestion interface."""

    st.title("Upload Documents")
    st.write(
        "Upload PDF documents to add them to your searchable "
        "document knowledge base."
    )

    document_service = DocumentService()
    ingestion_service = DocumentIngestionService()

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        return

    for uploaded_file in uploaded_files:
        if not document_service.is_valid_pdf(uploaded_file):
            st.error(
                f"{uploaded_file.name}: only PDF files are supported."
            )
            continue

        try:
            document_service.save_document(uploaded_file)

            with st.spinner(
                f"Processing {uploaded_file.name}..."
            ):
                result = ingestion_service.ingest_document(
                    uploaded_file.name
                )

            st.success(
                f"{uploaded_file.name} processed successfully."
            )

            st.caption(
                f"{result.pages} pages • "
                f"{result.chunks} chunks indexed"
            )

        except (OSError, ValueError, FileNotFoundError) as error:
            st.error(
                f"{uploaded_file.name}: processing failed — {error}"
            )