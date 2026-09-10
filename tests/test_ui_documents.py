"""Tests for Documents webpage rendering, interactions, and components (UI-09)."""

from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest

import pypdf
from streamlit.testing.v1 import AppTest

from app.services.document_service import DocumentMetadata
from app.ui import home as home_module
from app.ui.components import render_document_card
from app.ui.home import (
    TEXT_PREVIEW_LENGTH,
    _get_pdf_page_count,
    render_home_page,
)


# =========================================================================
# Fixtures & Helpers
# =========================================================================

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


def mock_columns(spec, *args, **kwargs):
    """Return a tuple of MagicMocks matching the length of column specification."""
    count = len(spec) if isinstance(spec, (list, tuple)) else int(spec)
    return tuple(MagicMock() for _ in range(count))


def _make_dummy_doc(
    filename: str = "test_doc.pdf",
    size_kb: float = 128.5,
    uploaded_at: datetime | None = None,
) -> DocumentMetadata:
    """Helper to construct dummy DocumentMetadata objects."""
    return DocumentMetadata(
        filename=filename,
        size_kb=size_kb,
        uploaded_at=uploaded_at or datetime(2026, 9, 10, 12, 0, 0),
    )


# =========================================================================
# 1. PDF Page Count Helper Tests (_get_pdf_page_count)
# =========================================================================

class TestGetPdfPageCount:
    """Test suite for _get_pdf_page_count utility."""

    def test_nonexistent_file_returns_one(self, monkeypatch) -> None:
        """If the PDF does not exist on disk, return 1 as a fallback."""
        _get_pdf_page_count.clear()
        monkeypatch.setattr(Path, "exists", lambda self: False)
        count = _get_pdf_page_count("nonexistent.pdf")
        assert count == 1

    def test_valid_pdf_returns_page_count(self, monkeypatch) -> None:
        """If a valid PDF exists, return the exact number of pages."""
        _get_pdf_page_count.clear()
        mock_reader = MagicMock()
        mock_reader.pages = [MagicMock(), MagicMock(), MagicMock()]

        monkeypatch.setattr(Path, "exists", lambda self: True)
        monkeypatch.setattr(pypdf, "PdfReader", lambda path: mock_reader)

        count = _get_pdf_page_count("valid.pdf")
        assert count == 3

    def test_corrupted_pdf_returns_one(self, monkeypatch) -> None:
        """If pypdf raises an exception reading corrupted content, fallback to 1."""
        _get_pdf_page_count.clear()

        def mock_broken_reader(path):
            raise pypdf.errors.PdfReadError("Corrupt stream")

        monkeypatch.setattr(Path, "exists", lambda self: True)
        monkeypatch.setattr(pypdf, "PdfReader", mock_broken_reader)

        count = _get_pdf_page_count("corrupted.pdf")
        assert count == 1


# =========================================================================
# 2. Document Card Component Unit Tests (render_document_card)
# =========================================================================

class TestDocumentCardComponent:
    """Test suite for the reusable render_document_card component."""

    def test_invalid_status_raises_value_error(self) -> None:
        """Document status must be 'ready' or 'processing', else ValueError."""
        with pytest.raises(ValueError, match="Document status must be 'ready' or 'processing'."):
            render_document_card(
                filename="test.pdf",
                pages=1,
                file_size="10 KB",
                uploaded_at="2026-09-10 12:00",
                status="invalid_status",
            )

    def test_ready_status_renders_badges(self, monkeypatch) -> None:
        """Ready status must render 'Indexed' and 'Ready for questions'."""
        html_calls = []
        monkeypatch.setattr("streamlit.html", lambda html: html_calls.append(html))
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.popover", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.download_button", lambda *args, **kwargs: False)

        result = render_document_card(
            filename="sample.pdf",
            pages=5,
            file_size="120 KB",
            uploaded_at="2026-09-10 12:00",
            status="ready",
        )

        all_html = "".join(html_calls)
        assert "document-status-ready" in all_html
        assert "Indexed" in all_html
        assert "Ready for questions" in all_html
        assert result == {"view_text": False, "delete": False, "view_details": False}

    def test_processing_status_renders_processing_dot(self, monkeypatch) -> None:
        """Processing status must render 'Processing...' badge."""
        html_calls = []
        monkeypatch.setattr("streamlit.html", lambda html: html_calls.append(html))
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.popover", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)

        render_document_card(
            filename="sample.pdf",
            pages=5,
            file_size="120 KB",
            uploaded_at="2026-09-10 12:00",
            status="processing",
        )

        all_html = "".join(html_calls)
        assert "document-status-processing" in all_html
        assert "Processing..." in all_html

    def test_popover_menu_actions_returned(self, monkeypatch) -> None:
        """Clicking popover details or menu delete returns True in action dict."""
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.popover", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)

        def mock_button(label, key=None, **kwargs):
            return "details" in (key or "")

        monkeypatch.setattr("streamlit.button", mock_button)
        monkeypatch.setattr("app.ui.components.render_button", lambda *args, **kwargs: False)

        res = render_document_card(
            filename="sample.pdf",
            pages=2,
            file_size="50 KB",
            uploaded_at="2026-09-10 12:00",
            status="ready",
            pdf_bytes=b"dummy_pdf",
        )
        assert res["view_details"] is True


# =========================================================================
# 3. Documents Page Rendering & Interaction Tests (render_home_page)
# =========================================================================

class TestDocumentsPage:
    """Test suite for render_home_page under various data states and interactions."""

    def test_clear_search_requested_resets_query_at_top(self, monkeypatch) -> None:
        """If _clear_search_requested is set in session_state, it resets doc_search_query."""
        session_state = MockSessionState({"_clear_search_requested": True, "doc_search_query": "old query"})
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [],
        )

        render_home_page()

        assert session_state["doc_search_query"] == ""
        assert session_state["_clear_search_requested"] is False

    def test_page_header_and_banner_rendered(self, monkeypatch) -> None:
        """Page header and intelligence banner HTML must always be rendered."""
        html_calls = []
        monkeypatch.setattr("streamlit.session_state", MockSessionState())
        monkeypatch.setattr("streamlit.html", lambda html: html_calls.append(html))
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [],
        )

        render_home_page()

        all_html = "".join(html_calls)
        assert "Your Documents" in all_html
        assert "Manage, view and explore your uploaded documents." in all_html
        assert "DOCUMENT INTELLIGENCE" in all_html
        assert "Your documents,<br>made searchable." in all_html
        assert "Secure. Private. Built for accuracy." in all_html

    def test_empty_documents_state_shows_info_callout(self, monkeypatch) -> None:
        """When list_documents() is empty, an info box is displayed prompting upload."""
        info_calls = []
        monkeypatch.setattr("streamlit.session_state", MockSessionState())
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.info", lambda msg: info_calls.append(msg))
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [],
        )

        render_home_page()

        assert len(info_calls) == 1
        assert "No documents have been uploaded yet." in info_calls[0]

    def test_document_count_singular_and_plural(self, monkeypatch) -> None:
        """Section counter displays '1 document' vs '2 documents'."""
        html_calls = []
        monkeypatch.setattr("streamlit.session_state", MockSessionState())
        monkeypatch.setattr("streamlit.html", lambda html: html_calls.append(html))
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("app.ui.home.render_document_card", lambda **kwargs: {})

        # 1 document
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("single.pdf")],
        )
        render_home_page()
        all_html = "".join(html_calls)
        assert "1 document" in all_html
        assert "1 documents" not in all_html

        # 2 documents
        html_calls.clear()
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("doc1.pdf"), _make_dummy_doc("doc2.pdf")],
        )
        render_home_page()
        all_html = "".join(html_calls)
        assert "2 documents" in all_html

    def test_search_filtering_with_matches(self, monkeypatch) -> None:
        """Searching filters documents and shows active filter tag."""
        rendered_cards = []
        html_calls = []
        monkeypatch.setattr("streamlit.session_state", MockSessionState())
        monkeypatch.setattr("streamlit.html", lambda html: html_calls.append(html))
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        # Search query entered: 'financial'
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "financial")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: rendered_cards.append(kwargs["filename"]) or {},
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [
                _make_dummy_doc("financial_report_2025.pdf"),
                _make_dummy_doc("product_handbook.pdf"),
            ],
        )

        render_home_page()

        assert rendered_cards == ["financial_report_2025.pdf"]
        all_html = "".join(html_calls)
        assert 'Filtering: "financial"' in all_html

    def test_search_filtering_no_matches_shows_empty_filter_state(self, monkeypatch) -> None:
        """Searching for non-matching term renders .documents-empty-filter-state and clear button."""
        html_calls = []
        monkeypatch.setattr("streamlit.session_state", MockSessionState())
        monkeypatch.setattr("streamlit.html", lambda html: html_calls.append(html))
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "unknown_term")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("alpha.pdf"), _make_dummy_doc("beta.pdf")],
        )

        render_home_page()

        all_html = "".join(html_calls)
        assert "documents-empty-filter-state" in all_html
        assert 'No documents matching "unknown_term"' in all_html

    def test_clear_search_button_triggers_reset(self, monkeypatch) -> None:
        """Clicking 'Clear search' button sets _clear_search_requested and triggers rerun."""
        session_state = MockSessionState()
        rerun_called = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "no_match")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.rerun", lambda: rerun_called.append(True))
        monkeypatch.setattr(
            "app.ui.home.render_button",
            lambda label, key=None, **kwargs: key == "clear_search_btn",
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("doc.pdf")],
        )

        render_home_page()

        assert session_state.get("_clear_search_requested") is True
        assert len(rerun_called) == 1

    def test_upload_document_navigation(self, monkeypatch) -> None:
        """Clicking '+ Upload Document' sets current_page to 'Upload' and calls rerun."""
        session_state = MockSessionState()
        rerun_called = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr(
            "streamlit.button",
            lambda label, key=None, **kwargs: key == "doc_upload_nav_btn",
        )
        monkeypatch.setattr("streamlit.rerun", lambda: rerun_called.append(True))
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [],
        )

        render_home_page()

        assert session_state["current_page"] == "Upload"
        assert len(rerun_called) == 1

    def test_toggle_view_details_drawer(self, monkeypatch) -> None:
        """Clicking view_details toggles show_details state and reruns."""
        session_state = MockSessionState()
        rerun_called = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.rerun", lambda: rerun_called.append(True))
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("test.pdf")],
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": True, "view_text": False, "delete": False},
        )

        render_home_page()

        assert session_state.get("show_details_test.pdf") is True
        assert len(rerun_called) == 1

    def test_close_details_drawer(self, monkeypatch) -> None:
        """Clicking 'Close Details' sets show_details to False and reruns."""
        session_state = MockSessionState({"show_details_test.pdf": True})
        rerun_called = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.rerun", lambda: rerun_called.append(True))
        monkeypatch.setattr(
            "app.ui.home.render_button",
            lambda label, key=None, **kwargs: key == "close_details_test.pdf",
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("test.pdf")],
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        assert session_state["show_details_test.pdf"] is False
        assert len(rerun_called) == 1

    def test_details_drawer_renders_all_six_items(self, monkeypatch) -> None:
        """When show_details is True, all 6 items render with labels and values."""
        session_state = MockSessionState({"show_details_contract.pdf": True})
        html_calls = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: html_calls.append(html))
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("contract.pdf", size_kb=256.0)],
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        all_html = "".join(html_calls)
        assert "documents-info-drawer" in all_html
        assert "documents-info-grid" in all_html
        assert "File Name" in all_html
        assert "contract.pdf" in all_html
        assert "File Format" in all_html
        assert "PDF Document" in all_html
        assert "Total Pages" in all_html
        assert "File Size" in all_html
        assert "256.0 KB" in all_html
        assert "Indexing Status" in all_html
        assert "Indexed &amp; Ready" in all_html
        assert "Storage Path" in all_html
        assert "data/uploads/contract.pdf" in all_html

    def test_view_text_drawer_success(self, monkeypatch) -> None:
        """When view_text is active, extracted text is fetched and previewed."""
        session_state = MockSessionState({"view_text_sample.pdf": True})
        text_areas = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.text_area", lambda label, value, **kwargs: text_areas.append(value))
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("sample.pdf")],
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.extract_document",
            lambda self, filename: [SimpleNamespace(page_content="Extracted line 1")],
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        assert len(text_areas) == 1
        assert "Extracted line 1" in text_areas[0]

    def test_view_text_drawer_truncation_caption(self, monkeypatch) -> None:
        """When extracted text exceeds TEXT_PREVIEW_LENGTH, a caption is displayed."""
        session_state = MockSessionState({"view_text_long.pdf": True})
        caption_calls = []
        long_content = "x" * (TEXT_PREVIEW_LENGTH + 500)
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.text_area", lambda *args, **kwargs: None)
        monkeypatch.setattr("streamlit.caption", lambda text: caption_calls.append(text))
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("long.pdf")],
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.extract_document",
            lambda self, filename: [SimpleNamespace(page_content=long_content)],
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        assert len(caption_calls) == 1
        assert f"first {TEXT_PREVIEW_LENGTH} characters" in caption_calls[0]

    def test_view_text_drawer_file_not_found(self, monkeypatch) -> None:
        """If document file is not found during extraction, display error and reset view_text."""
        session_state = MockSessionState({"view_text_missing.pdf": True})
        errors = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.error", lambda err: errors.append(err))
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("missing.pdf")],
        )

        def mock_extract(self, filename):
            raise FileNotFoundError("File does not exist")

        monkeypatch.setattr(
            "app.services.document_service.DocumentService.extract_document",
            mock_extract,
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        assert len(errors) == 1
        assert "missing.pdf could not be found." in errors[0]
        assert session_state["view_text_missing.pdf"] is False

    def test_view_text_drawer_extraction_os_error(self, monkeypatch) -> None:
        """If extraction fails with OSError or ValueError, display failure error."""
        session_state = MockSessionState({"view_text_corrupt.pdf": True})
        errors = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.error", lambda err: errors.append(err))
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("corrupt.pdf")],
        )

        def mock_extract(self, filename):
            raise OSError("I/O error during read")

        monkeypatch.setattr(
            "app.services.document_service.DocumentService.extract_document",
            mock_extract,
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        assert len(errors) == 1
        assert "Text extraction failed: I/O error during read" in errors[0]

    def test_delete_action_triggers_confirmation(self, monkeypatch) -> None:
        """Triggering delete action sets confirm_delete in session_state and reruns."""
        session_state = MockSessionState()
        rerun_called = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.rerun", lambda: rerun_called.append(True))
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("del.pdf")],
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": True},
        )

        render_home_page()

        assert session_state.get("confirm_delete_del.pdf") is True
        assert len(rerun_called) == 1

    def test_delete_cancel_removes_confirmation(self, monkeypatch) -> None:
        """Clicking Cancel in delete banner pops confirmation key and reruns."""
        session_state = MockSessionState({"confirm_delete_del.pdf": True})
        rerun_called = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.rerun", lambda: rerun_called.append(True))
        monkeypatch.setattr(
            "app.ui.home.render_button",
            lambda label, key=None, **kwargs: key == "cancel_del_del.pdf",
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("del.pdf")],
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        assert "confirm_delete_del.pdf" not in session_state
        assert len(rerun_called) == 1

    def test_delete_confirm_success(self, monkeypatch) -> None:
        """Confirming delete calls delete_document, clears state & cache, and reports success."""
        session_state = MockSessionState({
            "confirm_delete_target.pdf": True,
            "view_text_target.pdf": True,
            "show_details_target.pdf": True,
        })
        deleted_docs = []
        success_msgs = []
        rerun_called = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.success", lambda msg: success_msgs.append(msg))
        monkeypatch.setattr("streamlit.rerun", lambda: rerun_called.append(True))
        monkeypatch.setattr(
            "app.ui.home.render_button",
            lambda label, key=None, **kwargs: key == "confirm_del_target.pdf",
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("target.pdf")],
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.delete_document",
            lambda self, filename: deleted_docs.append(filename),
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        assert deleted_docs == ["target.pdf"]
        assert "confirm_delete_target.pdf" not in session_state
        assert "view_text_target.pdf" not in session_state
        assert "show_details_target.pdf" not in session_state
        assert len(success_msgs) == 1
        assert "target.pdf deleted." in success_msgs[0]
        assert len(rerun_called) == 1

    def test_delete_confirm_os_error(self, monkeypatch) -> None:
        """If delete_document raises OSError, an error is displayed without crash."""
        session_state = MockSessionState({"confirm_delete_target.pdf": True})
        error_msgs = []
        monkeypatch.setattr("streamlit.session_state", session_state)
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.error", lambda msg: error_msgs.append(msg))
        monkeypatch.setattr(
            "app.ui.home.render_button",
            lambda label, key=None, **kwargs: key == "confirm_del_target.pdf",
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [_make_dummy_doc("target.pdf")],
        )

        def mock_delete(self, filename):
            raise OSError("Permission denied")

        monkeypatch.setattr(
            "app.services.document_service.DocumentService.delete_document",
            mock_delete,
        )
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: {"view_details": False, "view_text": False, "delete": False},
        )

        render_home_page()

        assert len(error_msgs) == 1
        assert "target.pdf could not be deleted." in error_msgs[0]


# =========================================================================
# 4. Streamlit AppTest End-to-End Integration Tests
# =========================================================================

class TestStreamlitAppTestIntegration:
    """Integration test suite using Streamlit's official AppTest framework."""

    def test_app_loads_documents_page_by_default(self) -> None:
        """The app should launch cleanly and default to the Documents page."""
        at = AppTest.from_file(MAIN_SCRIPT_PATH, default_timeout=25)
        at.run()

        assert not at.exception
        assert at.session_state["current_page"] == "Documents"
        assert any(ti.key == "doc_search_query" for ti in at.text_input)
        assert any(b.key == "doc_upload_nav_btn" for b in at.button)

    def test_app_search_filter_and_clear_flow(self) -> None:
        """Typing a non-existent search query shows 'Clear search', which clears when clicked."""
        at = AppTest.from_file(MAIN_SCRIPT_PATH, default_timeout=25)
        at.run()
        assert not at.exception

        # Input non-matching search term
        search_box = at.text_input(key="doc_search_query")
        search_box.input("definitely_nonexistent_xyz").run()
        assert not at.exception

        # Clear search button must appear in empty filter state
        clear_buttons = [b for b in at.button if b.key == "clear_search_btn"]
        assert len(clear_buttons) == 1

        # Click clear search
        clear_buttons[0].click().run()
        assert not at.exception
        # Verified that doc_search_query was cleared back to empty string
        assert at.text_input(key="doc_search_query").value == ""


# =========================================================================
# 5. Edge Cases & Static Assets Tests
# =========================================================================

class TestEdgeCasesAndAssets:
    """Test suite for edge cases, special filenames, and asset helpers."""

    def test_special_characters_filename_safe_key(self, monkeypatch) -> None:
        """Filenames with spaces and special characters must not crash safe_key or rendering."""
        monkeypatch.setattr("streamlit.html", lambda html: None)
        container_mock = MagicMock()
        monkeypatch.setattr("streamlit.container", lambda key=None, **kwargs: container_mock)
        monkeypatch.setattr("streamlit.popover", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr("streamlit.download_button", lambda *args, **kwargs: False)

        result = render_document_card(
            filename="DocuMind Legal RAG Test (v2) #1 & 2026.pdf",
            pages=12,
            file_size="450 KB",
            uploaded_at="2026-09-10 14:30",
            status="ready",
        )
        assert result == {"view_text": False, "delete": False, "view_details": False}

    def test_search_query_whitespace_handling(self, monkeypatch) -> None:
        """Search query with leading and trailing whitespace is stripped before filtering."""
        rendered_cards = []
        monkeypatch.setattr("streamlit.session_state", MockSessionState())
        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: "   padded_doc   ")
        monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
        monkeypatch.setattr(
            "app.ui.home.render_document_card",
            lambda **kwargs: rendered_cards.append(kwargs["filename"]) or {},
        )
        monkeypatch.setattr(
            "app.services.document_service.DocumentService.list_documents",
            lambda self: [
                _make_dummy_doc("padded_doc.pdf"),
                _make_dummy_doc("other_doc.pdf"),
            ],
        )

        render_home_page()
        assert rendered_cards == ["padded_doc.pdf"]

    def test_load_image_base64_existing_and_missing(self) -> None:
        """load_image_base64 returns base64 string for existing image and empty string for missing."""
        from app.ui.styles import load_image_base64

        # Real visual in static/
        b64_visual = load_image_base64("Documents-Webpage-Visual.png")
        assert isinstance(b64_visual, str)
        assert len(b64_visual) > 0

        # Non-existent visual
        b64_missing = load_image_base64("nonexistent_image_xyz_123.png")
        assert b64_missing == ""

    def test_pdf_bytes_handling_in_card(self, monkeypatch) -> None:
        """render_document_card handles provided pdf_bytes vs nonexistent disk fallback cleanly."""
        download_rendered = []
        disabled_button_rendered = []

        monkeypatch.setattr("streamlit.html", lambda html: None)
        monkeypatch.setattr("streamlit.container", MagicMock())
        monkeypatch.setattr("streamlit.popover", MagicMock())
        monkeypatch.setattr("streamlit.columns", mock_columns)
        monkeypatch.setattr(
            "streamlit.button",
            lambda label, key=None, disabled=False, **kwargs: (
                disabled_button_rendered.append(key) if disabled else False
            ),
        )
        monkeypatch.setattr(
            "streamlit.download_button",
            lambda label, data, **kwargs: download_rendered.append(label) or False,
        )

        # 1. With explicit bytes -> triggers download_button
        render_document_card(
            filename="explicit.pdf",
            pages=1,
            file_size="10 KB",
            uploaded_at="2026-09-10 12:00",
            pdf_bytes=b"%PDF-1.4 test bytes",
        )
        assert len(download_rendered) == 1

        # 2. Without bytes and missing from disk -> triggers disabled button
        monkeypatch.setattr(
            Path,
            "exists",
            lambda self: False if "data/uploads" in str(self) else True,
        )
        render_document_card(
            filename="missing_on_disk.pdf",
            pages=1,
            file_size="10 KB",
            uploaded_at="2026-09-10 12:00",
            pdf_bytes=None,
        )
        assert any("dl-disabled" in k for k in disabled_button_rendered)


# =========================================================================
# 6. Styling Integrity & Design Specifications Tests
# =========================================================================

class TestStylesIntegrity:
    """Test suite verifying critical CSS selectors and design tokens for UI-09."""

    def test_styles_sheet_contains_ui09_selectors(self) -> None:
        """Ensure UI-09 CSS selectors and rules are present in styles.py."""
        from app.ui.styles import apply_global_styles

        # Read stylesheet source directly to inspect CSS template
        styles_file = Path(__file__).resolve().parent.parent / "app" / "ui" / "styles.py"
        content = styles_file.read_text(encoding="utf-8")

        # Header typography with requested margins
        assert ".documents-header" in content
        assert "margin-top: -1.5rem !important;" in content
        assert "margin-bottom: 2.35rem !important;" in content
        assert ".documents-title" in content
        assert ".documents-subtitle" in content

        # Empty state container
        assert ".documents-empty-filter-state" in content

        # Details drawer proportional grid
        assert ".documents-info-grid" in content
        assert "grid-template-columns: 1.8fr 0.72fr 0.88fr 0.88fr 0.95fr 2.55fr !important;" in content

        # Banner & Coral shield icon mask
        assert ".document-intelligence-banner" in content
        assert ".document-intelligence-icon-box::before" in content
        assert "#F96D57" in content or 'COLORS["coral"]' in content
