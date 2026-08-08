"""Document upload page rendering."""

import streamlit as st

from app.services.document_service import DocumentService


def render_upload_page() -> None:
    """Render the document upload interface."""

    st.title("Upload Documents")
    st.write("Upload PDF documents to add them to your document library.")

    document_service = DocumentService()

    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        return

    for uploaded_file in uploaded_files:
        if not document_service.is_valid_pdf(uploaded_file):
            st.error(f"{uploaded_file.name}: only PDF files are supported.")
            continue

        try:
            document_service.save_document(uploaded_file)
            st.success(f"{uploaded_file.name} uploaded successfully.")
        except OSError:
            st.error(f"{uploaded_file.name}: the file could not be saved.")
        except ValueError as error:
            st.error(f"{uploaded_file.name}: {error}")