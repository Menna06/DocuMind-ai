"""Document upload, management, and processing service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
from pathlib import Path
import shutil
from typing import TYPE_CHECKING

from langchain_core.documents import Document

from app.rag.loader import PDFDocumentLoader

if TYPE_CHECKING:
    from app.rag.vectorstore import DocumentVectorStore

logger = logging.getLogger(__name__)

UPLOAD_DIRECTORY = Path("data/uploads")


@dataclass
class DocumentMetadata:
    """Represents metadata about an uploaded document."""

    filename: str
    size_kb: float
    uploaded_at: datetime


class DocumentService:
    """Service responsible for document management and processing."""

    def __init__(
        self,
        vector_store: DocumentVectorStore | None = None,
    ) -> None:
        UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
        self.loader = PDFDocumentLoader()
        self.vector_store = vector_store

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
        """Delete a document if it exists and remove its vector embeddings."""

        safe_filename = Path(filename).name
        target = UPLOAD_DIRECTORY / safe_filename

        if target.exists():
            target.unlink()

        try:
            vector_store = self.vector_store
            if vector_store is None:
                from app.rag.vectorstore import DocumentVectorStore

                vector_store = DocumentVectorStore()

            vector_store.delete_document(safe_filename)
        except Exception as error:
            logger.warning(
                "Could not delete vectors for %s from vector store: %s",
                safe_filename,
                error,
            )

    def extract_document(self, filename: str) -> list[Document]:
        """Extract pages from a stored PDF."""

        safe_filename = Path(filename).name
        document_path = UPLOAD_DIRECTORY / safe_filename

        if not document_path.exists():
            raise FileNotFoundError(f"Document not found: {filename}")

        return self.loader.load(document_path)