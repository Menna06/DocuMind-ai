"""Home page rendering."""

import streamlit as st

from app.services.document_service import DocumentService


TEXT_PREVIEW_LENGTH = 2000


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

            extract_key = f"extract_{document.filename}"
            confirmation_key = f"confirm_delete_{document.filename}"

            if st.button(
                "Extract Text",
                key=extract_key,
            ):
                st.session_state["selected_document"] = document.filename

            if st.session_state.get("selected_document") == document.filename:
                try:
                    extracted_pages = document_service.extract_document(
                        document.filename
                    )

                    full_text = "\n\n".join(
                        page.page_content for page in extracted_pages
                    )

                    preview = full_text[:TEXT_PREVIEW_LENGTH]

                    st.caption(
                        f"{len(extracted_pages)} pages extracted"
                    )

                    st.text_area(
                        "Text Preview",
                        preview,
                        height=250,
                        disabled=True,
                        key=f"preview_{document.filename}",
                    )

                    if len(full_text) > TEXT_PREVIEW_LENGTH:
                        st.caption(
                            f"Showing the first {TEXT_PREVIEW_LENGTH} "
                            "characters."
                        )

                except FileNotFoundError:
                    st.error(
                        f"{document.filename} could not be found."
                    )
                    st.session_state.pop("selected_document", None)
                except (OSError, ValueError) as error:
                    st.error(
                        f"Text extraction failed: {error}"
                    )

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
                            document_service.delete_document(
                                document.filename
                            )
                            st.session_state.pop(
                                confirmation_key,
                                None,
                            )

                            if (
                                st.session_state.get("selected_document")
                                == document.filename
                            ):
                                st.session_state.pop(
                                    "selected_document",
                                    None,
                                )

                            st.success(
                                f"{document.filename} deleted."
                            )
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
                        st.session_state.pop(
                            confirmation_key,
                            None,
                        )
                        st.rerun()