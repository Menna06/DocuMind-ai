"""Home page rendering."""

import streamlit as st

from app.services.document_service import DocumentService


def render_home_page() -> None:
    """Render the document library."""

    st.title("DocuMind")
    st.write("Manage your uploaded documents.")

    document_service = DocumentService()
    documents = document_service.list_documents()

    if not documents:
        st.info("No documents have been uploaded yet.")
        return

    st.subheader("Your Documents")

    for document in documents:
        with st.container(border=True):
            st.write(document.filename)
            st.caption(
                f"{document.size_kb} KB • "
                f"Uploaded {document.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
            )

            confirmation_key = f"confirm_delete_{document.filename}"

            if st.button(
                "Delete",
                key=f"delete_{document.filename}",
            ):
                st.session_state[confirmation_key] = True

            if st.session_state.get(confirmation_key, False):
                st.warning(
                    f"Are you sure you want to delete {document.filename}?"
                )

                confirm_col, cancel_col = st.columns(2)

                with confirm_col:
                    if st.button(
                        "Confirm Delete",
                        key=f"confirm_{document.filename}",
                    ):
                        try:
                            document_service.delete_document(document.filename)
                            st.session_state.pop(confirmation_key, None)
                            st.success(f"{document.filename} deleted.")
                            st.rerun()
                        except OSError:
                            st.error(
                                f"{document.filename} could not be deleted."
                            )

                with cancel_col:
                    if st.button(
                        "Cancel",
                        key=f"cancel_{document.filename}",
                    ):
                        st.session_state.pop(confirmation_key, None)
                        st.rerun()