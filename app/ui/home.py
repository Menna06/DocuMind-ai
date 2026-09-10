"""Documents page rendering (UI-09)."""

from pathlib import Path
import pypdf
import streamlit as st

from app.services.document_service import DocumentService
from app.ui.components import render_button, render_document_card
from app.ui.styles import load_image_base64


TEXT_PREVIEW_LENGTH = 2000


@st.cache_data(show_spinner=False)
def _get_pdf_page_count(filename: str) -> int:
    """Return the page count for a stored PDF, cached for speed."""
    pdf_path = Path("data/uploads") / filename
    if not pdf_path.exists():
        return 1
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        return len(reader.pages)
    except Exception:
        return 1


def render_home_page() -> None:
    """Render the Documents page matching UI-09 design specifications."""

    # Handle pending clear-search request before widget instantiation
    if st.session_state.get("_clear_search_requested"):
        st.session_state["doc_search_query"] = ""
        st.session_state["_clear_search_requested"] = False

    # 1. Page Header
    st.html(
        """
        <div class="documents-header">
            <h1 class="documents-title">Your Documents</h1>
            <p class="documents-subtitle">Manage, view and explore your uploaded documents.</p>
        </div>
        """
    )

    # 2. Document Service & Filtering
    document_service = DocumentService()
    documents = document_service.list_documents()

    # 3. Action Bar: Search Input (left) + Upload Document Button (right) — Equal 1:1 balance
    with st.container(key="documents_action_bar"):
        col_search, col_upload = st.columns([1, 1], vertical_alignment="center")

        with col_search:
            with st.container(key="documents_search_box"):
                search_query = st.text_input(
                    "Search documents",
                    placeholder="Search documents...",
                    label_visibility="collapsed",
                    key="doc_search_query",
                )



        with col_upload:
            with st.container(key="documents_upload_col"):
                if st.button(
                    "+ Upload Document",
                    key="doc_upload_nav_btn",
                    use_container_width=True,
                ):
                    st.session_state.current_page = "Upload"
                    st.rerun()

    # 4. Search Filtering
    search_term = search_query.strip().lower() if search_query else ""
    if search_term:
        filtered_docs = [
            doc for doc in documents if search_term in doc.filename.lower()
        ]
    else:
        filtered_docs = documents

    # 5. Section Header: INDEXED DOCUMENTS & Counter
    doc_count = len(filtered_docs)
    count_label = (
        f"{doc_count} document" if doc_count == 1 else f"{doc_count} documents"
    )

    filter_tag_html = (
        f'<span class="documents-search-tag">Filtering: "{search_query}"</span>'
        if search_term
        else ""
    )

    st.html(
        f"""
        <div class="documents-section-header">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="documents-section-label">INDEXED DOCUMENTS</span>
                {filter_tag_html}
            </div>
            <span class="documents-section-count">{count_label}</span>
        </div>
        """
    )

    # 5. Document List or Empty State
    if not documents:
        with st.container(border=True):
            st.info(
                "No documents have been uploaded yet. "
                "Click '+ Upload Document' to upload your first PDF."
            )
    elif not filtered_docs:
        st.html(
            f"""
            <div class="documents-empty-filter-state">
                <div class="documents-empty-filter-title">No documents matching "{search_query}"</div>
                <div class="documents-empty-filter-sub">Check your search term or clear the filter to see all indexed documents.</div>
            </div>
            """
        )
        if render_button(
            "Clear search", variant="secondary", key="clear_search_btn"
        ):
            st.session_state["_clear_search_requested"] = True
            st.rerun()
    else:
        for doc in filtered_docs:
            pages = _get_pdf_page_count(doc.filename)
            file_size_str = f"{doc.size_kb} KB"
            uploaded_at_str = doc.uploaded_at.strftime("%Y-%m-%d %H:%M")

            actions = render_document_card(
                filename=doc.filename,
                pages=pages,
                file_size=file_size_str,
                uploaded_at=uploaded_at_str,
                status="ready",
                key=doc.filename,
            )

            # View Details Drawer Toggle
            if actions.get("view_details"):
                curr_details = st.session_state.get(
                    f"show_details_{doc.filename}", False
                )
                st.session_state[f"show_details_{doc.filename}"] = not curr_details
                st.rerun()

            if st.session_state.get(f"show_details_{doc.filename}", False):
                with st.container():
                    st.html(
                        f"""
                        <div class="documents-info-drawer">
                            <div class="documents-drawer-header">
                                <span class="documents-drawer-title">Document Details — {doc.filename}</span>
                                <span class="documents-drawer-meta">Uploaded {uploaded_at_str}</span>
                            </div>
                            <div class="documents-info-grid">
                                <div class="documents-info-item">
                                    <span class="documents-info-label">File Name</span>
                                    <span class="documents-info-value" title="{doc.filename}">{doc.filename}</span>
                                </div>
                                <div class="documents-info-item">
                                    <span class="documents-info-label">File Format</span>
                                    <span class="documents-info-value">PDF Document</span>
                                </div>
                                <div class="documents-info-item">
                                    <span class="documents-info-label">Total Pages</span>
                                    <span class="documents-info-value">{pages}</span>
                                </div>
                                <div class="documents-info-item">
                                    <span class="documents-info-label">File Size</span>
                                    <span class="documents-info-value">{file_size_str}</span>
                                </div>
                                <div class="documents-info-item">
                                    <span class="documents-info-label">Indexing Status</span>
                                    <span class="documents-info-value" style="color: #79B58A;">Indexed &amp; Ready</span>
                                </div>
                                <div class="documents-info-item">
                                    <span class="documents-info-label">Storage Path</span>
                                    <span class="documents-info-value" title="data/uploads/{doc.filename}">data/uploads/{doc.filename}</span>
                                </div>
                            </div>
                        </div>
                        """
                    )
                    col_close_det, _ = st.columns([1, 4])
                    with col_close_det:
                        if render_button(
                            "Close Details",
                            variant="ghost",
                            key=f"close_details_{doc.filename}",
                        ):
                            st.session_state[
                                f"show_details_{doc.filename}"
                            ] = False
                            st.rerun()

            # View Text Drawer Toggle
            if actions.get("view_text"):
                current_state = st.session_state.get(
                    f"view_text_{doc.filename}", False
                )
                st.session_state[f"view_text_{doc.filename}"] = not current_state
                st.rerun()

            if st.session_state.get(f"view_text_{doc.filename}", False):
                with st.container():
                    try:
                        extracted_pages = document_service.extract_document(
                            doc.filename
                        )
                        full_text = "\n\n".join(
                            page.page_content for page in extracted_pages
                        )
                        preview = full_text[:TEXT_PREVIEW_LENGTH]

                        st.html(
                            f"""
                            <div class="documents-text-drawer">
                                <div class="documents-drawer-header">
                                    <span class="documents-drawer-title">Extracted Text Preview — {doc.filename}</span>
                                    <span class="documents-drawer-meta">{len(extracted_pages)} pages extracted</span>
                                </div>
                            </div>
                            """
                        )

                        st.text_area(
                            f"Preview for {doc.filename}",
                            value=preview,
                            height=220,
                            disabled=True,
                            label_visibility="collapsed",
                            key=f"preview_area_{doc.filename}",
                        )

                        if len(full_text) > TEXT_PREVIEW_LENGTH:
                            st.caption(
                                f"Showing the first {TEXT_PREVIEW_LENGTH} characters."
                            )

                        col_close, _ = st.columns([1, 4])
                        with col_close:
                            if render_button(
                                "Close Preview",
                                variant="ghost",
                                key=f"close_preview_{doc.filename}",
                            ):
                                st.session_state[
                                    f"view_text_{doc.filename}"
                                ] = False
                                st.rerun()

                    except FileNotFoundError:
                        st.error(f"{doc.filename} could not be found.")
                        st.session_state[f"view_text_{doc.filename}"] = False
                    except (OSError, ValueError) as error:
                        st.error(f"Text extraction failed: {error}")

            # Delete confirmation
            if actions.get("delete"):
                st.session_state[f"confirm_delete_{doc.filename}"] = True
                st.rerun()

            if st.session_state.get(f"confirm_delete_{doc.filename}", False):
                with st.container():
                    st.html(
                        f"""
                        <div class="documents-delete-banner">
                            <div class="documents-delete-text">
                                Are you sure you want to delete <strong>{doc.filename}</strong>? This action cannot be undone.
                            </div>
                        </div>
                        """
                    )
                    col_confirm, col_cancel, _ = st.columns([1.2, 1, 3])
                    with col_confirm:
                        if render_button(
                            "Confirm Delete",
                            variant="danger",
                            key=f"confirm_del_{doc.filename}",
                        ):
                            try:
                                document_service.delete_document(doc.filename)
                                st.session_state.pop(
                                    f"confirm_delete_{doc.filename}", None
                                )
                                st.session_state.pop(
                                    f"view_text_{doc.filename}", None
                                )
                                st.session_state.pop(
                                    f"show_details_{doc.filename}", None
                                )
                                _get_pdf_page_count.clear()
                                st.success(f"{doc.filename} deleted.")
                                st.rerun()
                            except OSError:
                                st.error(
                                    f"{doc.filename} could not be deleted."
                                )
                    with col_cancel:
                        if render_button(
                            "Cancel",
                            variant="secondary",
                            key=f"cancel_del_{doc.filename}",
                        ):
                            st.session_state.pop(
                                f"confirm_delete_{doc.filename}", None
                            )
                            st.rerun()

    # 6. Document Intelligence Banner Card
    banner_b64 = load_image_base64("Documents-Webpage-Visual.png")
    img_tag = (
        f'<img src="data:image/png;base64,{banner_b64}" alt="Document Intelligence" />'
        if banner_b64
        else ""
    )

    st.html(
        f"""
        <div class="document-intelligence-banner">
            <div class="document-intelligence-content">
                <span class="document-intelligence-tag">DOCUMENT INTELLIGENCE</span>
                <div class="document-intelligence-headline">Your documents,<br>made searchable.</div>
                <p class="document-intelligence-desc">
                    DocuMind transforms uploaded PDFs into structured, searchable knowledge using semantic embeddings and diversified retrieval.
                </p>
                <div class="document-intelligence-badge">
                    <div class="document-intelligence-icon-box"></div>
                    <span>Secure. Private. Built for accuracy.</span>
                </div>
            </div>
            <div class="document-intelligence-visual">
                {img_tag}
            </div>
        </div>
        """
    )