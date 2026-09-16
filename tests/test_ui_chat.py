"""Tests for Ask DocuMind webpage rendering, interactions, and components (UI-10)."""

from pathlib import Path
from unittest.mock import MagicMock
import pytest

from langchain_core.documents import Document
from streamlit.testing.v1 import AppTest

from app.rag.pipeline import RAGQueryResult
from app.services.document_service import DocumentMetadata
from app.ui import chat as chat_module
from app.ui.chat import _get_pdf_icon_b64, render_chat_page

MAIN_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "app" / "main.py"


class MockSessionState(dict):
    """Session state mock supporting both dictionary and attribute access."""

    def __getattr__(self, name: str):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"st.session_state has no attribute '{name}'")

    def __setattr__(self, name: str, value):
        self[name] = value

    def __delattr__(self, name: str):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"st.session_state has no attribute '{name}'")


class DummyContextManager:
    """Mock context manager for st.container, st.form, and st.expander."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def mock_columns(spec, *args, **kwargs):
    """Return a tuple of MagicMocks matching the length of column specification."""
    count = len(spec) if isinstance(spec, (list, tuple)) else int(spec)
    return tuple(MagicMock() for _ in range(count))


@pytest.fixture
def mock_streamlit_ui(monkeypatch):
    """Ensure context managers do not taint the global Streamlit execution context in unit tests."""
    monkeypatch.setattr(chat_module.st, "container", lambda *a, **kw: DummyContextManager())
    monkeypatch.setattr(chat_module.st, "form", lambda *a, **kw: DummyContextManager())
    monkeypatch.setattr(chat_module.st, "form_submit_button", lambda *a, **kw: False)
    monkeypatch.setattr(chat_module.st, "expander", lambda *a, **kw: DummyContextManager())
    monkeypatch.setattr(chat_module.st, "columns", mock_columns)


# =========================================================================
# 1. PDF Icon Helper Tests
# =========================================================================

class TestPdfIconHelper:
    """Test suite for _get_pdf_icon_b64 utility."""

    def test_get_pdf_icon_b64_returns_string(self) -> None:
        """Icon loading helper should return a base64 string or empty string."""
        result = _get_pdf_icon_b64()
        assert isinstance(result, str)


# =========================================================================
# 2. Header, Subtitle & System Status Tests
# =========================================================================

class TestChatPageHeader:
    """Test suite for header and system status badge."""

    pytestmark = pytest.mark.usefixtures("mock_streamlit_ui")

    def test_header_renders_title_and_subtitle(self, monkeypatch) -> None:
        """Header should render serif title and two-line monospace subtitle."""
        html_calls = []
        monkeypatch.setattr(chat_module.st, "html", lambda markup: html_calls.append(markup))
        monkeypatch.setattr(chat_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        render_chat_page()

        joined_html = "".join(html_calls)
        assert "Ask DocuMind" in joined_html
        assert "ask-title" in joined_html
        assert "Ask any question about your documents." in joined_html
        assert "Answers are grounded in your document context." in joined_html

    def test_header_renders_system_ready_badge(self, monkeypatch) -> None:
        """Header should include the coral status dot and SYSTEM READY badge."""
        html_calls = []
        monkeypatch.setattr(chat_module.st, "html", lambda markup: html_calls.append(markup))
        monkeypatch.setattr(chat_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        render_chat_page()

        joined_html = "".join(html_calls)
        assert "SYSTEM READY" in joined_html
        assert "ask-top-bar" in joined_html
        assert "ask-status-pill" in joined_html
        assert "ask-status-dot" in joined_html


# =========================================================================
# 3. Question Input & Submission Tests
# =========================================================================

class TestQuestionSubmission:
    """Test suite for question submission, empty input, and RAG execution."""

    pytestmark = pytest.mark.usefixtures("mock_streamlit_ui")

    def test_empty_question_triggers_toast(self, monkeypatch) -> None:
        """Submitting an empty question should display a toast and skip query."""
        toast_mock = MagicMock()
        monkeypatch.setattr(chat_module.st, "toast", toast_mock)
        monkeypatch.setattr(chat_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(chat_module.st, "form_submit_button", lambda *a, **kw: True)
        monkeypatch.setattr(chat_module.st, "text_input", lambda *a, **kw: "   ")
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        mock_pipeline_cls = MagicMock()
        monkeypatch.setattr(chat_module, "RAGPipeline", mock_pipeline_cls)

        render_chat_page()

        toast_mock.assert_called_once_with("Please enter a question first.")
        mock_pipeline_cls.assert_not_called()

    def test_successful_query_stores_answer_and_sources(self, monkeypatch) -> None:
        """Submitting a valid question should execute the pipeline and store results."""
        session_state = MockSessionState()
        monkeypatch.setattr(chat_module.st, "session_state", session_state)
        monkeypatch.setattr(chat_module.st, "form_submit_button", lambda *a, **kw: True)
        monkeypatch.setattr(
            chat_module.st,
            "text_input",
            lambda *a, **kw: "What is the payment fee?",
        )
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="contract.pdf", size_kb=10.0, uploaded_at=None)],
        )

        dummy_docs = [
            Document(
                page_content="Fee is $84,000.",
                metadata={"source": "contract.pdf", "page": 0},
            )
        ]
        dummy_result = RAGQueryResult(
            answer="The fee is USD 84,000.",
            context="Fee is $84,000.",
            documents=dummy_docs,
        )

        mock_pipeline = MagicMock()
        mock_pipeline.query.return_value = dummy_result
        monkeypatch.setattr(chat_module, "RAGPipeline", lambda: mock_pipeline)

        render_chat_page()

        assert session_state["ask_last_query"] == "What is the payment fee?"
        assert session_state["ask_last_answer"] == "The fee is USD 84,000."
        assert session_state["ask_last_sources"] == dummy_docs
        assert session_state["ask_last_error"] is None
        mock_pipeline.query.assert_called_once_with("What is the payment fee?")


# =========================================================================
# 4. Answer & Evidence Display Tests
# =========================================================================

class TestAnswerAndEvidenceDisplay:
    """Test suite for rendering the generated answer and retrieved evidence cards."""

    pytestmark = pytest.mark.usefixtures("mock_streamlit_ui")

    def test_answer_section_renders_when_present(self, monkeypatch) -> None:
        """When an answer exists in session state, render reusable answer component."""
        html_calls = []
        markdown_calls = []
        monkeypatch.setattr(chat_module.st, "html", lambda markup: html_calls.append(markup))
        monkeypatch.setattr(chat_module.st, "markdown", lambda text, **kw: markdown_calls.append(text))
        monkeypatch.setattr(
            chat_module.st,
            "session_state",
            MockSessionState(
                ask_last_answer="Total fee was $84,000 in 3 milestones.",
                ask_last_sources=[],
            ),
        )
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        render_chat_page()

        joined_markdown = "".join(markdown_calls)
        assert "documind-answer-wrapper" in joined_markdown
        assert "Answer" in joined_markdown
        assert "Total fee was $84,000 in 3 milestones." in joined_markdown

    def test_evidence_cards_render_with_filename_and_page(self, monkeypatch) -> None:
        """When sources exist, render EVIDENCE cards with filename, 1-indexed page, and link arrow."""
        html_calls = []
        monkeypatch.setattr(chat_module.st, "html", lambda markup: html_calls.append(markup))
        monkeypatch.setattr(chat_module.st, "markdown", MagicMock())
        monkeypatch.setattr(chat_module.st, "columns", mock_columns)

        docs = [
            Document(
                page_content="Excerpt 1 content and agreement terms.",
                metadata={"source": "data/uploads/DocuMind_Legal.pdf", "page": 0},
            ),
            Document(
                page_content="Excerpt 2 content and milestone payments.",
                metadata={"source": "data/uploads/DocuMind_Legal.pdf", "page": 1},
            ),
        ]
        monkeypatch.setattr(
            chat_module.st,
            "session_state",
            MockSessionState(
                ask_last_answer="Excerpt 1 content and agreement terms with Excerpt 2 content and milestone payments.",
                ask_last_sources=docs,
                ask_last_query="What are the agreement terms and milestone payments?",
            ),
        )
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="DocuMind_Legal.pdf", size_kb=10.0, uploaded_at=None)],
        )

        render_chat_page()

        joined_html = "".join(html_calls)
        assert "EVIDENCE" in joined_html
        assert "DocuMind_Legal.pdf" in joined_html
        assert "Page 1" in joined_html
        assert "Page 2" in joined_html
        assert "↗" in joined_html

    def test_not_found_answer_does_not_display_info_message(self, monkeypatch) -> None:
        """Not-found answers should not display a misleading missing-sources callout."""
        info_mock = MagicMock()
        monkeypatch.setattr(chat_module.st, "info", info_mock)
        monkeypatch.setattr(chat_module.st, "markdown", MagicMock())
        monkeypatch.setattr(
            chat_module.st,
            "session_state",
            MockSessionState(
                ask_last_answer="The requested information is not available in the provided documents.",
                ask_last_sources=[],
            ),
        )
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [
                DocumentMetadata(
                    filename="doc.pdf",
                    size_kb=10.0,
                    uploaded_at=None,
                )
            ],
        )

        render_chat_page()

        info_mock.assert_not_called()

    def test_no_sources_displays_info_message(self, monkeypatch) -> None:
        """When answer exists but sources list is empty, display info callout."""
        info_mock = MagicMock()
        monkeypatch.setattr(chat_module.st, "info", info_mock)
        monkeypatch.setattr(chat_module.st, "markdown", MagicMock())
        monkeypatch.setattr(
            chat_module.st,
            "session_state",
            MockSessionState(
                ask_last_answer="General knowledge answer.",
                ask_last_sources=[],
            ),
        )
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        render_chat_page()

        info_mock.assert_called_once_with(
            "No supporting documents were retrieved for this question."
        )


# =========================================================================
# 5. Error Handling Tests
# =========================================================================

class TestChatErrorHandling:
    """Test suite for handling ValueError, OSError, and general exceptions."""

    pytestmark = pytest.mark.usefixtures("mock_streamlit_ui")

    def test_value_error_handling(self, monkeypatch) -> None:
        """ValueError from pipeline should be captured and displayed via st.error."""
        error_mock = MagicMock()
        monkeypatch.setattr(chat_module.st, "error", error_mock)
        session_state = MockSessionState()
        monkeypatch.setattr(chat_module.st, "session_state", session_state)
        monkeypatch.setattr(chat_module.st, "form_submit_button", lambda *a, **kw: True)
        monkeypatch.setattr(chat_module.st, "text_input", lambda *a, **kw: "Invalid query")
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        mock_pipeline = MagicMock()
        mock_pipeline.query.side_effect = ValueError("Query cannot be empty")
        monkeypatch.setattr(chat_module, "RAGPipeline", lambda: mock_pipeline)

        render_chat_page()

        assert session_state["ask_last_error"] == "Query cannot be empty"
        assert session_state["ask_last_answer"] is None
        error_mock.assert_called_once_with("Query cannot be empty")

    def test_os_error_handling(self, monkeypatch) -> None:
        """OSError from vectorstore access should be captured with friendly prefix."""
        error_mock = MagicMock()
        monkeypatch.setattr(chat_module.st, "error", error_mock)
        session_state = MockSessionState()
        monkeypatch.setattr(chat_module.st, "session_state", session_state)
        monkeypatch.setattr(chat_module.st, "form_submit_button", lambda *a, **kw: True)
        monkeypatch.setattr(chat_module.st, "text_input", lambda *a, **kw: "Query")
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        mock_pipeline = MagicMock()
        mock_pipeline.query.side_effect = OSError("Permission denied")
        monkeypatch.setattr(chat_module, "RAGPipeline", lambda: mock_pipeline)

        render_chat_page()

        assert "Unable to access the document store" in session_state["ask_last_error"]
        error_mock.assert_called_once_with(
            "Unable to access the document store: Permission denied"
        )

    def test_unexpected_exception_handling(self, monkeypatch) -> None:
        """Unexpected exceptions should be caught without crashing the application."""
        error_mock = MagicMock()
        monkeypatch.setattr(chat_module.st, "error", error_mock)
        session_state = MockSessionState()
        monkeypatch.setattr(chat_module.st, "session_state", session_state)
        monkeypatch.setattr(chat_module.st, "form_submit_button", lambda *a, **kw: True)
        monkeypatch.setattr(chat_module.st, "text_input", lambda *a, **kw: "Query")
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        mock_pipeline = MagicMock()
        mock_pipeline.query.side_effect = RuntimeError("API key quota exhausted")
        monkeypatch.setattr(chat_module, "RAGPipeline", lambda: mock_pipeline)

        render_chat_page()

        assert "An error occurred while generating the answer" in session_state["ask_last_error"]
        error_mock.assert_called_once()


# =========================================================================
# 6. Empty State & Navigation Tests
# =========================================================================

class TestChatEmptyState:
    """Test suite for zero-documents guidance and Upload navigation."""

    pytestmark = pytest.mark.usefixtures("mock_streamlit_ui")

    def test_empty_documents_shows_guidance_card(self, monkeypatch) -> None:
        """When no documents are indexed and no answer exists, show guidance card."""
        html_calls = []
        monkeypatch.setattr(chat_module.st, "html", lambda markup: html_calls.append(markup))
        monkeypatch.setattr(chat_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(chat_module.st, "columns", mock_columns)
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [],
        )

        render_chat_page()

        joined_html = "".join(html_calls)
        assert "No documents indexed yet" in joined_html
        assert "ask-empty-state" in joined_html

    def test_empty_state_upload_button_navigates_to_upload(self, monkeypatch) -> None:
        """Clicking the Upload button in the empty state navigates to Upload page."""
        session_state = MockSessionState()
        rerun_mock = MagicMock()
        monkeypatch.setattr(chat_module.st, "session_state", session_state)
        monkeypatch.setattr(chat_module.st, "rerun", rerun_mock)
        monkeypatch.setattr(chat_module.st, "button", lambda *a, **kw: True)
        monkeypatch.setattr(chat_module.st, "columns", mock_columns)
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [],
        )

        render_chat_page()

        assert session_state.current_page == "Upload"
        rerun_mock.assert_called_once()


# =========================================================================
# 7. Footer Disclaimer Tests
# =========================================================================

class TestChatFooterDisclaimer:
    """Test suite for footer disclaimer."""

    pytestmark = pytest.mark.usefixtures("mock_streamlit_ui")

    def test_footer_disclaimer_rendered(self, monkeypatch) -> None:
        """Footer should render shield icon and Gemini/MMR grounding disclaimer."""
        html_calls = []
        monkeypatch.setattr(chat_module.st, "html", lambda markup: html_calls.append(markup))
        monkeypatch.setattr(chat_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(
            chat_module.DocumentService,
            "list_documents",
            lambda self: [DocumentMetadata(filename="doc.pdf", size_kb=10.0, uploaded_at=None)],
        )

        render_chat_page()

        joined_html = "".join(html_calls)
        assert "ask-footer-disclaimer" in joined_html
        assert "ask-shield-icon" in joined_html
        assert "grounded in the most relevant document chunks retrieved via MMR." in joined_html


# =========================================================================
# 8. Streamlit AppTest End-to-End Integration
# =========================================================================

class TestStreamlitAppTestIntegration:
    """End-to-end simulation of navigating to Ask DocuMind and verifying UI."""

    def test_app_navigates_to_ask_documind(self) -> None:
        """AppTest should load, navigate to Ask DocuMind, and render without exceptions."""
        at = AppTest.from_file(MAIN_SCRIPT_PATH, default_timeout=25)
        at.run()
        assert not at.exception

        # Find and click the Ask DocuMind sidebar navigation button
        ask_btn = None
        for button in at.sidebar.button:
            if button.label == "Ask DocuMind" or button.key == "workspace_ask":
                ask_btn = button
                break

        assert ask_btn is not None
        ask_btn.click().run()
        assert not at.exception

        # Verify page state
        assert at.session_state["current_page"] == "Ask DocuMind"

        # Verify Ask DocuMind widgets render cleanly
        assert any(ti.key == "ask_question_input" for ti in at.text_input)
        assert any(b.label == "Ask →" for b in at.button)
