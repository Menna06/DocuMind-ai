"""Tests for Upload Document webpage rendering, interactions, and components (UI-11)."""

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock
import pytest

from streamlit.testing.v1 import AppTest

from app.rag.ingestion import IngestionResult
from app.services.document_service import DocumentMetadata
from app.ui import upload as upload_module
from app.ui.upload import (
    INGESTION_PHASES,
    _format_date,
    _format_size,
    _get_pdf_page_count,
    render_stepper_html,
    render_upload_page,
)

MAIN_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "app" / "main.py"


@pytest.fixture(autouse=True)
def no_stepper_sleep(monkeypatch):
    """Disable visual animation sleep during automated test execution."""
    monkeypatch.setattr(upload_module, "_stepper_sleep", lambda s: None)


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
    """Mock context manager for st.container, st.form, and st.columns."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def mock_columns(spec, *args, **kwargs):
    """Return a tuple of MagicMocks matching the length of column specification."""
    count = len(spec) if isinstance(spec, (list, tuple)) else int(spec)
    return tuple(MagicMock() for _ in range(count))


def _make_dummy_doc(
    filename: str = "test_case.pdf",
    size_kb: float = 120.0,
    uploaded_at: datetime | None = None,
) -> DocumentMetadata:
    """Helper to construct dummy DocumentMetadata objects."""
    return DocumentMetadata(
        filename=filename,
        size_kb=size_kb,
        uploaded_at=uploaded_at or datetime(2026, 8, 12, 23, 40),
    )


# =========================================================================
# 1. Header & Status Pill Tests
# =========================================================================

class TestUploadHeaderAndStatus:
    """Test top bar, system ready status, and page header."""

    def test_header_and_status_rendered(self, monkeypatch) -> None:
        html_calls: list[str] = []
        monkeypatch.setattr(
            upload_module.st,
            "html",
            lambda markup: html_calls.append(markup),
        )
        monkeypatch.setattr(
            upload_module.st, "session_state", MockSessionState()
        )
        monkeypatch.setattr(
            upload_module.st, "file_uploader", MagicMock(return_value=None)
        )
        monkeypatch.setattr(
            upload_module.st, "container", lambda **kwargs: DummyContextManager()
        )
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [],
        )

        render_upload_page()

        joined = "\n".join(html_calls)
        assert "ask-top-bar" in joined
        assert "ask-status-pill" in joined
        assert "SYSTEM READY" in joined
        assert "Upload Document" in joined
        assert "Upload PDFs and let DocuMind extract" in joined


# =========================================================================
# 2. Dropzone Tests
# =========================================================================

class TestUploadDropzone:
    """Test file uploader integration and dropzone container."""

    def test_file_uploader_called_with_pdf_types(self, monkeypatch) -> None:
        file_uploader_mock = MagicMock(return_value=None)
        container_keys: list[str] = []

        def fake_container(**kwargs):
            if "key" in kwargs:
                container_keys.append(kwargs["key"])
            return DummyContextManager()

        monkeypatch.setattr(upload_module.st, "file_uploader", file_uploader_mock)
        monkeypatch.setattr(upload_module.st, "container", fake_container)
        monkeypatch.setattr(upload_module.st, "html", MagicMock())
        monkeypatch.setattr(
            upload_module.st, "session_state", MockSessionState()
        )
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [],
        )

        render_upload_page()

        file_uploader_mock.assert_called_once()
        _, kwargs = file_uploader_mock.call_args
        assert kwargs.get("type") == ["pdf"]
        assert kwargs.get("key") == "upload_pdf_file"
        assert kwargs.get("label_visibility") == "collapsed"
        assert "upload_dropzone_wrapper" in container_keys

    def test_dropzone_resets_with_dynamic_key_and_displays_success_message(self, monkeypatch) -> None:
        """When an upload completes, the uploader resets to a fresh key and renders the success alert."""
        file_uploader_mock = MagicMock(return_value=None)
        success_mock = MagicMock()
        session_state = MockSessionState(
            _uploader_nonce=1,
            _upload_success_message="sample.pdf uploaded and indexed successfully (3 pages, 12 chunks).",
        )

        monkeypatch.setattr(upload_module.st, "session_state", session_state)
        monkeypatch.setattr(upload_module.st, "file_uploader", file_uploader_mock)
        monkeypatch.setattr(upload_module.st, "success", success_mock)
        monkeypatch.setattr(upload_module.st, "html", MagicMock())
        monkeypatch.setattr(upload_module.st, "container", lambda **kwargs: DummyContextManager())
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [],
        )

        render_upload_page()

        # Uploader should mount with reset dynamic key
        file_uploader_mock.assert_called_once()
        _, kwargs = file_uploader_mock.call_args
        assert kwargs.get("key") == "upload_pdf_file_1"

        # Success message should be displayed and cleared from session state
        success_mock.assert_called_once_with("sample.pdf uploaded and indexed successfully (3 pages, 12 chunks).")
        assert "_upload_success_message" not in session_state


# =========================================================================
# 3. Recent Uploads Tests (Reusing render_document_card)
# =========================================================================

class TestRecentUploads:
    """Test rendering of recent documents, metadata, and reusable component integration."""

    def test_empty_recent_uploads_displays_guidance(self, monkeypatch) -> None:
        html_calls: list[str] = []
        monkeypatch.setattr(
            upload_module.st,
            "html",
            lambda markup: html_calls.append(markup),
        )
        monkeypatch.setattr(
            upload_module.st, "session_state", MockSessionState()
        )
        monkeypatch.setattr(
            upload_module.st, "file_uploader", MagicMock(return_value=None)
        )
        monkeypatch.setattr(
            upload_module.st, "container", lambda **kwargs: DummyContextManager()
        )
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [],
        )

        render_upload_page()

        joined = "\n".join(html_calls)
        assert "0 documents uploaded" in joined
        assert "No documents uploaded yet" in joined

    def test_recent_uploads_delegates_to_reusable_render_document_card(self, monkeypatch) -> None:
        card_calls: list[dict] = []

        def fake_render_card(**kwargs):
            card_calls.append(kwargs)
            return {}

        monkeypatch.setattr(upload_module, "render_document_card", fake_render_card)
        monkeypatch.setattr(upload_module.st, "html", MagicMock())
        monkeypatch.setattr(upload_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(upload_module.st, "file_uploader", MagicMock(return_value=None))
        monkeypatch.setattr(upload_module.st, "container", lambda **kwargs: DummyContextManager())
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [
                _make_dummy_doc("alpha.pdf", size_kb=1024.0),
                _make_dummy_doc("beta.pdf", size_kb=6.98),
            ],
        )
        monkeypatch.setattr(
            upload_module,
            "_get_pdf_page_count",
            lambda fn: 2 if "beta" in fn else 5,
        )

        render_upload_page()

        assert len(card_calls) == 2
        assert card_calls[0]["filename"] == "alpha.pdf"
        assert card_calls[0]["pages"] == 5
        assert card_calls[0]["file_size"] == "1024.0 KB"
        assert card_calls[0]["status"] == "ready"

        assert card_calls[1]["filename"] == "beta.pdf"
        assert card_calls[1]["pages"] == 2
        assert card_calls[1]["file_size"] == "6.98 KB"
        assert card_calls[1]["status"] == "ready"

    def test_recent_uploads_renders_processing_status_during_active_ingestion(self, monkeypatch) -> None:
        card_calls: list[dict] = []

        def fake_render_card(**kwargs):
            card_calls.append(kwargs)
            return {}

        dummy_file = MagicMock()
        dummy_file.name = "active_processing.pdf"
        dummy_file.getvalue.return_value = b"%PDF-1.4 test"

        monkeypatch.setattr(upload_module, "render_document_card", fake_render_card)
        monkeypatch.setattr(upload_module.st, "html", MagicMock())
        monkeypatch.setattr(upload_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(upload_module.st, "file_uploader", MagicMock(return_value=dummy_file))
        monkeypatch.setattr(upload_module.st, "container", lambda **kwargs: DummyContextManager())
        monkeypatch.setattr(upload_module.st, "empty", lambda: MagicMock())
        monkeypatch.setattr(upload_module.st, "rerun", MagicMock())
        monkeypatch.setattr(upload_module.st, "success", MagicMock())
        monkeypatch.setattr(upload_module.DocumentService, "is_valid_pdf", lambda self, f: True)
        monkeypatch.setattr(upload_module.DocumentService, "save_document", MagicMock())
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [
                _make_dummy_doc("active_processing.pdf", size_kb=6.98),
                _make_dummy_doc("existing.pdf", size_kb=120.0),
            ],
        )
        monkeypatch.setattr(
            upload_module.DocumentIngestionService,
            "ingest_document",
            lambda self, fn: IngestionResult(fn, 1, 2, ["id1"]),
        )

        render_upload_page()

        assert len(card_calls) == 2
        assert card_calls[0]["filename"] == "active_processing.pdf"
        assert card_calls[0]["status"] == "processing"
        assert card_calls[1]["filename"] == "existing.pdf"
        assert card_calls[1]["status"] == "ready"

    def test_delete_action_triggers_service_deletion(self, monkeypatch) -> None:
        delete_mock = MagicMock()
        rerun_mock = MagicMock()
        success_mock = MagicMock()

        monkeypatch.setattr(upload_module.DocumentService, "delete_document", delete_mock)
        monkeypatch.setattr(upload_module.st, "rerun", rerun_mock)
        monkeypatch.setattr(upload_module.st, "success", success_mock)
        monkeypatch.setattr(upload_module.st, "html", MagicMock())
        session_state = MockSessionState(_last_ingested_file="target.pdf")
        session_state["confirm_delete_target.pdf"] = True
        monkeypatch.setattr(upload_module.st, "session_state", session_state)
        monkeypatch.setattr(upload_module.st, "file_uploader", MagicMock(return_value=None))
        monkeypatch.setattr(upload_module.st, "container", lambda **kwargs: DummyContextManager())
        monkeypatch.setattr(upload_module.st, "columns", mock_columns)
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [_make_dummy_doc("target.pdf")],
        )
        monkeypatch.setattr(
            upload_module,
            "render_document_card",
            lambda **kwargs: {},
        )
        # Click "Confirm Delete" button
        monkeypatch.setattr(
            upload_module,
            "render_button",
            lambda label, **kwargs: label == "Confirm Delete",
        )

        render_upload_page()

        delete_mock.assert_called_once_with("target.pdf")
        rerun_mock.assert_called_once()
        assert "_last_ingested_file" not in upload_module.st.session_state


# =========================================================================
# 4. Ingestion Progress & Visibility Rules
# =========================================================================

class TestIngestionProgressVisibilityAndStepper:
    """Verify stepper phases, absence of technical jargon, and visibility logic."""

    def test_ingestion_progress_not_visible_when_idle(self, monkeypatch) -> None:
        """Stepper MUST NOT be rendered when no document is being uploaded."""
        html_calls: list[str] = []
        monkeypatch.setattr(
            upload_module.st,
            "html",
            lambda markup: html_calls.append(markup),
        )
        monkeypatch.setattr(upload_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(upload_module.st, "file_uploader", MagicMock(return_value=None))
        monkeypatch.setattr(upload_module.st, "container", lambda **kwargs: DummyContextManager())
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [_make_dummy_doc("existing.pdf")],
        )
        monkeypatch.setattr(upload_module, "render_document_card", lambda **kwargs: {})

        render_upload_page()

        joined = "\n".join(html_calls)
        assert "INGESTION PROGRESS" not in joined

    def test_ingestion_phases_no_technical_jargon(self) -> None:
        """Verify user-facing text uses friendly names and NO developer jargon."""
        forbidden_jargon = [
            "chunk",
            "chunking",
            "chunks",
            "embedding",
            "embeddings",
            "vector",
            "vectors",
            "vectorstore",
            "chroma",
        ]

        expected_phase_names = [
            "Upload",
            "Analysis",
            "Structuring",
            "Processing",
            "Ready",
        ]

        actual_phase_names = [p["name"] for p in INGESTION_PHASES]
        assert actual_phase_names == expected_phase_names

        for phase in INGESTION_PHASES:
            full_text = f"{phase['name']} {phase['description']}".lower()
            for jargon in forbidden_jargon:
                assert jargon not in full_text, (
                    f"Forbidden technical jargon '{jargon}' found in phase: {phase}"
                )

    def test_render_stepper_html_states(self) -> None:
        """Verify completed, progress, and pending markup across phases."""
        html_p2 = render_stepper_html(active_phase=2, is_complete=False)
        assert "upload-stepper-card" in html_p2
        assert "1. Upload" in html_p2
        assert "2. Analysis" in html_p2
        assert "3. Structuring" in html_p2
        assert "4. Processing" in html_p2
        assert "5. Ready" in html_p2

        assert '<span class="upload-step-pill completed">Completed</span>' in html_p2
        assert '<span class="upload-step-pill progress">In Progress</span>' in html_p2
        assert '<span class="upload-step-pill pending">Pending</span>' in html_p2

        html_complete = render_stepper_html(active_phase=5, is_complete=True)
        assert "In Progress" not in html_complete
        assert "Pending" not in html_complete
        assert html_complete.count("Completed") == 5


# =========================================================================
# 5. File Upload & Ingestion Flow Tests
# =========================================================================

class TestUploadIngestionFlow:
    """Test full upload handling, validation, and ingestion service calls."""

    def test_valid_pdf_triggers_save_and_ingestion(self, monkeypatch) -> None:
        save_mock = MagicMock()
        ingest_mock = MagicMock(return_value=IngestionResult("sample.pdf", 3, 12, ["id1"]))
        rerun_mock = MagicMock()
        success_mock = MagicMock()
        empty_slot = MagicMock()
        html_calls: list[str] = []

        dummy_file = MagicMock()
        dummy_file.name = "sample.pdf"

        monkeypatch.setattr(upload_module.DocumentService, "is_valid_pdf", lambda self, f: True)
        monkeypatch.setattr(upload_module.DocumentService, "save_document", save_mock)
        monkeypatch.setattr(upload_module.DocumentIngestionService, "ingest_document", ingest_mock)
        monkeypatch.setattr(upload_module.DocumentService, "list_documents", lambda self: [])
        monkeypatch.setattr(upload_module.st, "file_uploader", MagicMock(return_value=dummy_file))
        monkeypatch.setattr(upload_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(upload_module.st, "html", lambda markup: html_calls.append(markup))
        monkeypatch.setattr(upload_module.st, "container", lambda **kwargs: DummyContextManager())
        monkeypatch.setattr(upload_module.st, "empty", lambda: empty_slot)
        monkeypatch.setattr(upload_module.st, "rerun", rerun_mock)
        monkeypatch.setattr(upload_module.st, "success", success_mock)

        render_upload_page()

        save_mock.assert_called_once_with(dummy_file)
        ingest_mock.assert_called_once_with("sample.pdf")
        success_mock.assert_called_once()
        assert "sample.pdf" in success_mock.call_args[0][0]
        assert "3 pages" in success_mock.call_args[0][0]
        assert upload_module.st.session_state["_last_ingested_file"] == "sample.pdf"
        assert upload_module.st.session_state.get("_uploader_nonce") == 1
        assert "_upload_success_message" in upload_module.st.session_state
        rerun_mock.assert_called_once()

        # Ingestion progress header should be shown during active processing
        joined = "\n".join(html_calls)
        assert "INGESTION PROGRESS" in joined

    def test_ingestion_flows_through_all_five_phases(self, monkeypatch) -> None:
        stepper_renders: list[int] = []

        def spy_render_stepper(active_phase: int = 5, is_complete: bool = True) -> str:
            stepper_renders.append(active_phase)
            return f"<div>Phase {active_phase} is_complete={is_complete}</div>"

        dummy_file = MagicMock()
        dummy_file.name = "flow_test.pdf"

        monkeypatch.setattr(upload_module, "render_stepper_html", spy_render_stepper)
        monkeypatch.setattr(upload_module.DocumentService, "is_valid_pdf", lambda self, f: True)
        monkeypatch.setattr(upload_module.DocumentService, "save_document", MagicMock())
        monkeypatch.setattr(
            upload_module.DocumentIngestionService,
            "ingest_document",
            lambda self, fn: IngestionResult(fn, 2, 4, ["id1"]),
        )
        monkeypatch.setattr(upload_module.DocumentService, "list_documents", lambda self: [])
        monkeypatch.setattr(upload_module.st, "file_uploader", MagicMock(return_value=dummy_file))
        monkeypatch.setattr(upload_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(upload_module.st, "html", MagicMock())
        monkeypatch.setattr(upload_module.st, "container", lambda **kwargs: DummyContextManager())
        monkeypatch.setattr(upload_module.st, "empty", lambda: MagicMock())
        monkeypatch.setattr(upload_module.st, "rerun", MagicMock())
        monkeypatch.setattr(upload_module.st, "success", MagicMock())

        render_upload_page()

        # Stepper must sequentially advance through all 5 phases
        assert stepper_renders == [1, 2, 3, 4, 5]

    def test_invalid_pdf_displays_error(self, monkeypatch) -> None:
        save_mock = MagicMock()
        error_mock = MagicMock()

        dummy_file = MagicMock()
        dummy_file.name = "notes.txt"

        monkeypatch.setattr(upload_module.DocumentService, "is_valid_pdf", lambda self, f: False)
        monkeypatch.setattr(upload_module.DocumentService, "save_document", save_mock)
        monkeypatch.setattr(upload_module.DocumentService, "list_documents", lambda self: [])
        monkeypatch.setattr(upload_module.st, "file_uploader", MagicMock(return_value=dummy_file))
        monkeypatch.setattr(upload_module.st, "session_state", MockSessionState())
        monkeypatch.setattr(upload_module.st, "html", MagicMock())
        monkeypatch.setattr(upload_module.st, "container", lambda **kwargs: DummyContextManager())
        monkeypatch.setattr(upload_module.st, "error", error_mock)

        render_upload_page()

        save_mock.assert_not_called()
        error_mock.assert_called_once()
        assert "only PDF files are supported" in error_mock.call_args[0][0]


# =========================================================================
# 6. Security Callout Tests (No Emojis, Coral SVG Icon)
# =========================================================================

class TestSecurityCallout:
    """Verify presence of security and privacy message with vector SVG and NO emojis."""

    def test_security_callout_rendered_with_no_emojis(self, monkeypatch) -> None:
        html_calls: list[str] = []
        monkeypatch.setattr(
            upload_module.st,
            "html",
            lambda markup: html_calls.append(markup),
        )
        monkeypatch.setattr(
            upload_module.st, "session_state", MockSessionState()
        )
        monkeypatch.setattr(
            upload_module.st, "file_uploader", MagicMock(return_value=None)
        )
        monkeypatch.setattr(
            upload_module.st, "container", lambda **kwargs: DummyContextManager()
        )
        monkeypatch.setattr(
            upload_module.DocumentService,
            "list_documents",
            lambda self: [],
        )

        render_upload_page()

        joined = "\n".join(html_calls)
        assert "upload-security-callout" in joined
        assert "upload-security-icon-img" in joined or "upload-shield-svg" in joined
        assert "processed securely and privately" in joined
        assert "available for Q&A once indexing is complete" in joined

        # Explicitly verify NO emojis are present
        assert "🛡" not in joined
        assert "🔒" not in joined


# =========================================================================
# 7. Helper Utilities Tests
# =========================================================================

class TestUploadHelpers:
    """Test format helpers."""

    def test_format_size_kb_and_mb(self) -> None:
        assert _format_size(500.0) == "500.00 KB"
        assert _format_size(1024.0) == "1.00 MB"
        assert _format_size(2048.5) == "2.00 MB"

    def test_format_date(self) -> None:
        dt = datetime(2026, 8, 12, 14, 30)
        assert _format_date(dt) == "2026-08-12 14:30"
        assert _format_date(None) == "Unknown"


# =========================================================================
# 8. AppTest Integration Navigation
# =========================================================================

class TestUploadAppTest:
    """Integration test using Streamlit AppTest runner."""

    def test_upload_page_renders_in_apptest(self) -> None:
        at = AppTest.from_file(str(MAIN_SCRIPT_PATH))
        at.run()
        assert not at.exception

        # Switch to upload page if radio is present
        if at.radio:
            radio = at.radio[0]
            if "Upload" in radio.options:
                radio.select("Upload").run()
                assert not at.exception
                assert len(at.file_uploader) > 0
