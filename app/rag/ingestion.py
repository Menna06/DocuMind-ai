"""Document ingestion pipeline for indexing uploaded PDFs."""

from dataclasses import dataclass

from langchain_core.documents import Document

from app.rag.chunker import DocumentChunker
from app.rag.vectorstore import DocumentVectorStore
from app.services.document_service import DocumentService


class DocumentIngestionError(Exception):
    """Raised when document ingestion cannot be completed."""


@dataclass(frozen=True)
class IngestionResult:
    """Represent the outcome of indexing a document."""

    filename: str
    pages: int
    chunks: int
    document_ids: list[str]


class DocumentIngestionService:
    """Coordinate PDF extraction, chunking, and vector-store indexing."""

    def __init__(self) -> None:
        self.document_service = DocumentService()
        self.chunker = DocumentChunker()
        self.vector_store = DocumentVectorStore()

    def ingest_document(self, filename: str) -> IngestionResult:
        """Extract, chunk, and index a stored PDF document."""

        try:
            pages = self.document_service.extract_document(filename)
        except (FileNotFoundError, ValueError) as error:
            raise DocumentIngestionError(
                f"Unable to extract document '{filename}': {error}"
            ) from error
        except Exception as error:
            raise DocumentIngestionError(
                f"Failed to process document '{filename}'."
            ) from error

        if not pages:
            return IngestionResult(
                filename=filename,
                pages=0,
                chunks=0,
                document_ids=[],
            )

        try:
            chunks = self.chunker.split_documents(pages)
        except Exception as error:
            raise DocumentIngestionError(
                f"Failed to chunk document '{filename}'."
            ) from error

        if not chunks:
            return IngestionResult(
                filename=filename,
                pages=len(pages),
                chunks=0,
                document_ids=[],
            )

        try:
            document_ids = self.vector_store.add_documents(chunks)
        except Exception as error:
            raise DocumentIngestionError(
                f"Failed to index document '{filename}'."
            ) from error

        return IngestionResult(
            filename=filename,
            pages=len(pages),
            chunks=len(chunks),
            document_ids=document_ids,
        )