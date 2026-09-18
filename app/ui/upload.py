"""Document upload and ingestion interface (UI-11)."""

from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path
import time
import pypdf
import streamlit as st

from app.rag.ingestion import DocumentIngestionService
from app.services.document_service import DocumentMetadata, DocumentService
from app.ui.components import render_button, render_document_card
from app.ui.theme import COLORS


INGESTION_PHASES = [
    {
        "number": "1",
        "name": "Upload",
        "description": "File received",
        "icon": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>""",
    },
    {
        "number": "2",
        "name": "Analysis",
        "description": "Reading document",
        "icon": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>""",
    },
    {
        "number": "3",
        "name": "Structuring",
        "description": "Organizing content",
        "icon": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>""",
    },
    {
        "number": "4",
        "name": "Processing",
        "description": "Preparing intelligent search",
        "icon": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>""",
    },
    {
        "number": "5",
        "name": "Ready",
        "description": "Available for questions",
        "icon": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>""",
    },
]


def _stepper_sleep(seconds: float) -> None:
    """Pause briefly during ingestion phase transitions for smooth visual feedback."""
    time.sleep(seconds)


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


def _format_size(size_kb: float) -> str:
    """Format file size in KB or MB."""
    if size_kb >= 1024:
        return f"{size_kb / 1024:.2f} MB"
    return f"{size_kb:.2f} KB"


def _format_date(dt: datetime | None) -> str:
    """Format datetime for display."""
    if dt is None:
        return "Unknown"
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M")
    return str(dt)


def render_stepper_html(active_phase: int = 5, is_complete: bool = True) -> str:
    """Generate HTML for the 5-phase ingestion progress stepper."""
    if is_complete or active_phase >= 5:
        fill_width = "80%"
    elif active_phase <= 1:
        fill_width = "0%"
    elif active_phase == 2:
        fill_width = "20%"
    elif active_phase == 3:
        fill_width = "40%"
    elif active_phase == 4:
        fill_width = "60%"
    else:
        fill_width = "80%"

    steps_html: list[str] = []
    for i, phase in enumerate(INGESTION_PHASES, start=1):
        if is_complete or i < active_phase:
            circle_class = "completed"
            text_class = "active"
            pill_html = '<span class="upload-step-pill completed">Completed</span>'
            icon_html = phase["icon"]
        elif i == active_phase:
            circle_class = "progress"
            text_class = "active"
            pill_html = '<span class="upload-step-pill progress">In Progress</span>'
            icon_html = phase["icon"]
        else:
            circle_class = "pending"
            text_class = "muted"
            pill_html = '<span class="upload-step-pill pending">Pending</span>'
            icon_html = phase["icon"]

        step_markup = f"""
        <div class="upload-step-item">
            <div class="upload-step-circle {circle_class}">
                {icon_html}
            </div>
            <div class="upload-step-name {text_class}">
                {phase["number"]}. {phase["name"]}
            </div>
            <div class="upload-step-desc {text_class}">
                {phase["description"]}
            </div>
            {pill_html}
        </div>
        """
        steps_html.append(step_markup)

    all_steps = "\n".join(steps_html)
    return f"""
    <div class="upload-stepper-card">
        <div class="upload-stepper-track">
            <div class="upload-stepper-line-bg"></div>
            <div class="upload-stepper-line-fill" style="width: {fill_width};"></div>
            {all_steps}
        </div>
    </div>
    """


def render_upload_page() -> None:
    """Render the document upload and ingestion interface."""

    # 1. Top Bar & Page Header (positioned exactly as on Ask DocuMind)
    st.html(
        """
        <div class="ask-top-bar">
            <div class="ask-status-pill">
                <span class="ask-status-dot"></span>
                SYSTEM READY
            </div>
        </div>
        <div class="upload-header">
            <h1 class="upload-title">Upload Document</h1>
            <p class="upload-subtitle">
                Upload PDFs and let DocuMind extract, index and make them ready for intelligent search.
            </p>
        </div>
        """
    )

    # 2. Services Initialization
    document_service = DocumentService()
    ingestion_service = DocumentIngestionService()

    # 3. Dropzone Area
    uploader_nonce = st.session_state.get("_uploader_nonce", 0)
    uploader_key = f"upload_pdf_file_{uploader_nonce}" if uploader_nonce else "upload_pdf_file"
    with st.container(key="upload_dropzone_wrapper"):
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            key=uploader_key,
            label_visibility="collapsed",
        )

    # Success message banner (displayed on rerun after upload completion)
    if "_upload_success_message" in st.session_state:
        with st.container(key="upload_success_toast"):
            st.success(st.session_state.pop("_upload_success_message"))

    # 4. Check for active upload / processing
    is_processing = False
    processing_filename: str | None = None

    if uploaded_file is not None:
        last_ingested = st.session_state.get("_last_ingested_file")
        if last_ingested != uploaded_file.name:
            if not document_service.is_valid_pdf(uploaded_file):
                st.error(f"{uploaded_file.name}: only PDF files are supported.")
            else:
                is_processing = True
                processing_filename = uploaded_file.name
                try:
                    document_service.save_document(uploaded_file)
                    _get_pdf_page_count.clear()
                except Exception as save_err:
                    st.error(f"Failed to save document: {save_err}")
                    is_processing = False
                    processing_filename = None

    # 5. Recent Uploads Section (reusing the exact render_document_card component)
    documents = document_service.list_documents()
    if is_processing and processing_filename:
        # Ensure processing document is in documents list and displayed first
        if processing_filename not in [d.filename for d in documents]:
            file_bytes = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else b""
            size_kb = round(len(file_bytes) / 1024, 2) if file_bytes else 0.0
            documents.insert(
                0,
                DocumentMetadata(
                    filename=processing_filename,
                    size_kb=size_kb,
                    uploaded_at=datetime.now(),
                ),
            )
        else:
            documents.sort(key=lambda d: 0 if d.filename == processing_filename else 1)

    doc_count = len(documents)
    count_label = f"{doc_count} document{'s' if doc_count != 1 else ''} uploaded"

    st.html(
        f"""
        <div class="upload-section-row">
            <div class="upload-section-title">RECENT UPLOADS</div>
            <div class="upload-section-count">{count_label}</div>
        </div>
        """
    )

    if documents:
        for doc in documents:
            pages = _get_pdf_page_count(doc.filename)
            file_size_str = f"{doc.size_kb} KB"
            uploaded_at_str = (
                doc.uploaded_at.strftime("%Y-%m-%d %H:%M")
                if isinstance(doc.uploaded_at, datetime)
                else str(doc.uploaded_at)
            )
            card_status = "processing" if (is_processing and doc.filename == processing_filename) else "ready"

            actions = render_document_card(
                filename=doc.filename,
                pages=pages,
                file_size=file_size_str,
                uploaded_at=uploaded_at_str,
                status=card_status,
                key=f"upload_{doc.filename}",
            )

            # Details Drawer Toggle
            if actions.get("view_details"):
                curr = st.session_state.get(f"show_details_{doc.filename}", False)
                st.session_state[f"show_details_{doc.filename}"] = not curr
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
                            st.session_state[f"show_details_{doc.filename}"] = False
                            st.rerun()

            # View Text Drawer Toggle
            if actions.get("view_text"):
                curr_text = st.session_state.get(f"view_text_{doc.filename}", False)
                st.session_state[f"view_text_{doc.filename}"] = not curr_text
                st.rerun()

            if st.session_state.get(f"view_text_{doc.filename}", False):
                with st.container():
                    try:
                        extracted_pages = document_service.extract_document(doc.filename)
                        full_text = "\n\n".join(p.page_content for p in extracted_pages)
                        preview = full_text[:2000]
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
                        if len(full_text) > 2000:
                            st.caption("Showing the first 2000 characters.")
                        col_close_txt, _ = st.columns([1, 4])
                        with col_close_txt:
                            if render_button(
                                "Close Preview",
                                variant="ghost",
                                key=f"close_preview_{doc.filename}",
                            ):
                                st.session_state[f"view_text_{doc.filename}"] = False
                                st.rerun()
                    except Exception as error:
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
                                st.session_state.pop(f"confirm_delete_{doc.filename}", None)
                                st.session_state.pop(f"show_details_{doc.filename}", None)
                                st.session_state.pop(f"view_text_{doc.filename}", None)
                                if st.session_state.get("_last_ingested_file") == doc.filename:
                                    st.session_state.pop("_last_ingested_file", None)
                                _get_pdf_page_count.clear()
                                st.success(f"{doc.filename} deleted.")
                                st.rerun()
                            except OSError:
                                st.error(f"{doc.filename} could not be deleted.")
                    with col_cancel:
                        if render_button(
                            "Cancel",
                            variant="secondary",
                            key=f"cancel_del_{doc.filename}",
                        ):
                            st.session_state.pop(f"confirm_delete_{doc.filename}", None)
                            st.rerun()
    else:
        st.html(
            """
            <div class="upload-recent-card" style="justify-content: center; color: #77717B; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; padding: 20px;">
                No documents uploaded yet. Upload a PDF above to get started.
            </div>
            """
        )

    # 6. Ingestion Progress Section (ONLY VISIBLE WHEN ACTIVELY PROCESSING)
    if is_processing and processing_filename:
        st.html(
            """
            <div class="upload-section-row" style="margin-top: 1.5rem;">
                <div class="upload-section-title">
                    INGESTION PROGRESS <span class="upload-stepper-dot">●</span>
                </div>
            </div>
            """
        )
        stepper_placeholder = st.empty()
        try:
            # Phase 1: Upload (File received)
            stepper_placeholder.html(render_stepper_html(active_phase=1, is_complete=False))
            _stepper_sleep(0.35)

            # Phase 2: Analysis (Reading document)
            stepper_placeholder.html(render_stepper_html(active_phase=2, is_complete=False))
            _stepper_sleep(0.4)

            # Phase 3: Structuring (Organizing content)
            stepper_placeholder.html(render_stepper_html(active_phase=3, is_complete=False))
            _stepper_sleep(0.4)

            # Phase 4: Processing (Preparing intelligent search / vector indexing)
            stepper_placeholder.html(render_stepper_html(active_phase=4, is_complete=False))
            result = ingestion_service.ingest_document(processing_filename)
            _stepper_sleep(0.4)

            # Phase 5: Ready (Available for questions — complete)
            stepper_placeholder.html(render_stepper_html(active_phase=5, is_complete=True))
            _stepper_sleep(0.7)

            st.session_state["_last_ingested_file"] = processing_filename
            success_msg = f"{processing_filename} uploaded and indexed successfully ({result.pages} pages, {result.chunks} chunks)."
            st.session_state["_upload_success_message"] = success_msg
            st.session_state["_uploader_nonce"] = uploader_nonce + 1
            st.session_state.pop(uploader_key, None)
            st.session_state.pop("upload_pdf_file", None)
            with st.container(key="upload_success_toast"):
                st.success(success_msg)
            st.rerun()
        except Exception as error:
            st.error(f"{processing_filename}: processing failed — {error}")

    # 7. Bottom Security & Privacy Callout (NO EMOJIS, exact orange shield icon with SVG fallback)
    shield_path = Path("static/icons/security-shield.png")
    coral_hex = COLORS.get("coral", "#F96D57")
    if shield_path.exists():
        encoded_shield = base64.b64encode(shield_path.read_bytes()).decode("utf-8")
        shield_icon_html = (
            f'<img src="data:image/png;base64,{encoded_shield}" '
            f'alt="Security" '
            f'class="upload-security-icon-img" />'
        )
    else:
        shield_icon_html = (
            f'<svg class="upload-shield-svg" width="20" height="22" viewBox="0 0 24 24" fill="none" stroke="{coral_hex}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;">'
            f'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
            f'</svg>'
        )

    st.html(
        f"""
        <div class="upload-security-callout">
            {shield_icon_html}
            <div class="upload-security-text">
                Your document is processed securely and privately.<br/>
                It will be available for Q&A once indexing is complete.
            </div>
        </div>
        """
    )
