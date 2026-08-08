"""Tests for document management services."""

from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock

from langchain_core.documents import Document

import app.services.document_service as document_service_module
from app.services.document_service import DocumentService

class FakeUploadedFile(BytesIO):
    """Provide a minimal uploaded-file interface for testing."""

    def __init__(self, filename: str, content: bytes) -> None:
        super().__init__(content)
        self.name = filename


def test_valid_pdf_is_accepted() -> None:
    """A PDF file should pass validation."""

    service = DocumentService()
    uploaded_file = SimpleNamespace(name="document.pdf")

    assert service.is_valid_pdf(uploaded_file) is True


def test_non_pdf_is_rejected() -> None:
    """A non-PDF file should fail validation."""

    service = DocumentService()
    uploaded_file = SimpleNamespace(name="document.txt")

    assert service.is_valid_pdf(uploaded_file) is False


def test_document_is_saved(tmp_path, monkeypatch) -> None:
    """An uploaded PDF should be saved to the configured directory."""

    monkeypatch.setattr(
        document_service_module,
        "UPLOAD_DIRECTORY",
        tmp_path,
    )

    service = DocumentService()
    uploaded_file = FakeUploadedFile(
        "document.pdf",
        b"PDF test content",
    )

    saved_path = service.save_document(uploaded_file)

    assert saved_path == tmp_path / "document.pdf"
    assert saved_path.exists()
    assert saved_path.read_bytes() == b"PDF test content"


def test_document_metadata_is_returned(tmp_path, monkeypatch) -> None:
    """Stored PDFs should appear in the document metadata list."""

    monkeypatch.setattr(
        document_service_module,
        "UPLOAD_DIRECTORY",
        tmp_path,
    )

    document_path = tmp_path / "document.pdf"
    document_path.write_bytes(b"PDF test content")

    service = DocumentService()
    documents = service.list_documents()

    assert len(documents) == 1
    assert documents[0].filename == "document.pdf"
    assert documents[0].size_kb > 0
    assert documents[0].uploaded_at is not None


def test_document_is_deleted(tmp_path, monkeypatch) -> None:
    """A stored document should be removed when deleted."""

    monkeypatch.setattr(
        document_service_module,
        "UPLOAD_DIRECTORY",
        tmp_path,
    )

    document_path = tmp_path / "document.pdf"
    document_path.write_bytes(b"PDF test content")

    service = DocumentService()
    service.delete_document("document.pdf")

    assert not document_path.exists()


def test_filename_is_restricted_to_storage_directory(
    tmp_path,
    monkeypatch,
) -> None:
    """File paths supplied by users should not escape the storage directory."""

    monkeypatch.setattr(
        document_service_module,
        "UPLOAD_DIRECTORY",
        tmp_path,
    )

    service = DocumentService()
    uploaded_file = FakeUploadedFile(
        "../../outside.pdf",
        b"PDF test content",
    )

    saved_path = service.save_document(uploaded_file)

    assert saved_path == tmp_path / "outside.pdf"
    assert saved_path.parent == tmp_path
    assert saved_path.exists()

def test_extract_document_returns_loaded_pages(tmp_path, monkeypatch):
    monkeypatch.setattr(
        document_service_module,
        "UPLOAD_DIRECTORY",
        tmp_path,
    )

    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"test pdf content")

    expected_documents = [
        Document(
            page_content="First page content",
            metadata={"page": 0},
        ),
        Document(
            page_content="Second page content",
            metadata={"page": 1},
        ),
    ]

    service = document_service_module.DocumentService()
    service.loader = Mock()
    service.loader.load.return_value = expected_documents

    documents = service.extract_document("sample.pdf")

    assert len(documents) == 2
    assert documents[0].page_content == "First page content"
    assert documents[1].page_content == "Second page content"
    service.loader.load.assert_called_once_with(pdf_path)


def test_extract_document_raises_for_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        document_service_module,
        "UPLOAD_DIRECTORY",
        tmp_path,
    )

    service = document_service_module.DocumentService()

    try:
        service.extract_document("missing.pdf")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError as error:
        assert "Document not found: missing.pdf" in str(error)