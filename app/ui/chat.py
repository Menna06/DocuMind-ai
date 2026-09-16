"""Ask DocuMind Q&A interface and grounded evidence rendering (UI-10)."""

from pathlib import Path
import streamlit as st

from app.rag.citations import extract_evidence_sources, is_not_found_answer
from app.rag.pipeline import RAGPipeline
from app.services.document_service import DocumentService
from app.ui.components import render_answer_display
from app.ui.styles import load_image_base64


@st.cache_data(show_spinner=False)
def _get_pdf_icon_b64() -> str:
    """Return cached base64-encoded PDF visual icon."""
    return load_image_base64("icons/PDF-visual.png")


def render_chat_page() -> None:
    """Render the Ask DocuMind interface matching UI-10 design specifications."""

    st.html(
        """
        <div class="ask-top-bar">
            <div class="ask-status-pill">
                <span class="ask-status-dot"></span>
                SYSTEM READY
            </div>
        </div>
        <div class="ask-header">
            <h1 class="ask-title">Ask DocuMind</h1>
            <p class="ask-subtitle">
                Ask any question about your documents.<br/>
                Answers are grounded in your document context.
            </p>
        </div>
        """
    )

    document_service = DocumentService()
    indexed_documents = document_service.list_documents()

    with st.container(key="ask_prompt_card"):
        with st.form(key="ask_prompt_form", border=False):
            question_text = st.text_input(
                "Question",
                value=st.session_state.get("ask_input_text", ""),
                placeholder="Type your question here...",
                label_visibility="collapsed",
                key="ask_question_input",
            )

            col_hint, col_btn = st.columns([1, 1], vertical_alignment="center")
            with col_hint:
                st.html(
                    """
                    <div class="ask-card-hint">
                        <span>✦</span> Press Enter to ask
                    </div>
                    """
                )
            with col_btn:
                with st.container(key="ask_submit_btn_wrapper"):
                    submit_clicked = st.form_submit_button(
                        "Ask →",
                        type="primary",
                    )

    if submit_clicked:
        query = question_text.strip()
        if not query:
            st.toast("Please enter a question first.")
        else:
            st.session_state["ask_input_text"] = query
            st.session_state["ask_last_query"] = query

            try:
                pipeline = RAGPipeline()
                with st.spinner("Searching your documents..."):
                    result = pipeline.query(query)

                st.session_state["ask_last_answer"] = result.answer
                st.session_state["ask_last_sources"] = result.documents
                st.session_state["ask_last_error"] = None

            except ValueError as error:
                st.session_state["ask_last_error"] = str(error)
                st.session_state["ask_last_answer"] = None
                st.session_state["ask_last_sources"] = []

            except OSError as error:
                st.session_state["ask_last_error"] = (
                    f"Unable to access the document store: {error}"
                )
                st.session_state["ask_last_answer"] = None
                st.session_state["ask_last_sources"] = []

            except Exception as error:
                st.session_state["ask_last_error"] = (
                    f"An error occurred while generating the answer: {error}"
                )
                st.session_state["ask_last_answer"] = None
                st.session_state["ask_last_sources"] = []

    last_error = st.session_state.get("ask_last_error")
    if last_error:
        st.error(last_error)

    answer = st.session_state.get("ask_last_answer")
    if answer:
        render_answer_display(answer=answer)

    sources = st.session_state.get("ask_last_sources", [])
    if answer and sources:
        last_query = st.session_state.get("ask_last_query", "")
        display_docs = extract_evidence_sources(
            answer=answer,
            query=last_query,
            documents=sources,
            max_sources=3,
        )

        if display_docs:
            st.html(
                """
                <div class="ask-section-header">
                    <span>EVIDENCE</span>
                    <span class="ask-section-dot"></span>
                </div>
                """
            )

            with st.container(key="ask_evidence_box"):
                cols = st.columns(len(display_docs) if len(display_docs) < 3 else 3)
                pdf_b64 = _get_pdf_icon_b64()

                img_markup = (
                    f'<img src="data:image/png;base64,{pdf_b64}" alt="PDF" />'
                    if pdf_b64
                    else """<svg width="18" height="20" viewBox="0 0 18 20" fill="none">
                    <path d="M10.5 1H3C1.89543 1 1 1.89543 1 3V17C1 18.1046 1.89543 19 3 19H15C16.1046 19 17 18.1046 17 17V7.5L10.5 1Z" stroke="#A855F7" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M10.5 1V7.5H17" stroke="#A855F7" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                    <text x="4" y="14" fill="#A855F7" font-size="5" font-family="monospace" font-weight="bold">PDF</text>
                    </svg>"""
                )

                for col, doc in zip(cols, display_docs):
                    with col:
                        source = doc.metadata.get("source", "Document.pdf")
                        filename = Path(source).name if source else "Document.pdf"
                        page = doc.metadata.get("page")

                        if page is not None:
                            try:
                                page_display = int(page) + 1
                            except (ValueError, TypeError):
                                page_display = 1
                        else:
                            page_display = 1

                        card_html = f"""
                        <div class="ask-evidence-card">
                            <div class="ask-evidence-top">
                                <div class="ask-pdf-box">
                                    {img_markup}
                                </div>
                                <span class="ask-evidence-filename" title="{filename}">{filename}</span>
                            </div>
                            <div class="ask-evidence-bottom">
                                <span>Page {page_display}</span>
                                <span class="ask-evidence-arrow">↗</span>
                            </div>
                        </div>
                        """
                        st.html(card_html)

                        excerpt = doc.page_content.strip()
                        if excerpt:
                            with st.expander(f"Excerpt • {filename} (p. {page_display})"):
                                st.html(f'<div class="ask-chunk-preview">{excerpt}</div>')

        elif not is_not_found_answer(answer):
            st.info("No supporting documents were retrieved for this question.")

    elif answer and not sources:
        if not is_not_found_answer(answer):
            st.info("No supporting documents were retrieved for this question.")

    if not indexed_documents and not answer:
        st.html(
            """
            <div class="ask-empty-state">
                <div class="ask-empty-title">No documents indexed yet</div>
                <div class="ask-empty-desc">Upload PDF documents to your workspace to start asking questions.</div>
            </div>
            """
        )
        col_pad_l, col_cta, col_pad_r = st.columns([1, 1, 1])
        with col_cta:
            if st.button(
                "+ Upload Document",
                key="ask_nav_upload_btn",
                use_container_width=True,
            ):
                st.session_state.current_page = "Upload"
                st.rerun()

    st.html(
        """
        <div class="ask-footer-disclaimer">
            <span class="ask-shield-icon"></span>
            <span>Answers are generated using Gemini and grounded in the most relevant document chunks retrieved via MMR.</span>
        </div>
        """
    )
