"""Document upload and management service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import shutil


UPLOAD_DIRECTORY = Path("data/uploads")


@dataclass
class DocumentMetadata:
    """Represents metadata about an uploaded document."""

    filename: str
    size_kb: float
    uploaded_at: datetime


class DocumentService:
    """Service responsible for document management."""

    def __init__(self) -> None:
        UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

    def is_valid_pdf(self, uploaded_file) -> bool:
        """Return True if the uploaded file is a PDF."""

        if uploaded_file is None:
            return False

        return uploaded_file.name.lower().endswith(".pdf")

    def save_document(self, uploaded_file) -> Path:
        """Save an uploaded PDF to local storage."""

        if not self.is_valid_pdf(uploaded_file):
            raise ValueError("Only PDF files are supported.")

        filename = Path(uploaded_file.name).name
        destination = UPLOAD_DIRECTORY / filename

        with destination.open("wb") as file:
            shutil.copyfileobj(uploaded_file, file)

        return destination

    def list_documents(self) -> list[DocumentMetadata]:
        """Return metadata for every uploaded document."""

        documents: list[DocumentMetadata] = []

        for pdf in sorted(UPLOAD_DIRECTORY.glob("*.pdf")):
            stat = pdf.stat()

            documents.append(
                DocumentMetadata(
                    filename=pdf.name,
                    size_kb=round(stat.st_size / 1024, 2),
                    uploaded_at=datetime.fromtimestamp(stat.st_mtime),
                )
            )

        return documents

    def delete_document(self, filename: str) -> None:
        """Delete a document if it exists."""

        safe_filename = Path(filename).name
        target = UPLOAD_DIRECTORY / safe_filename

        if target.exists():
            target.unlink()