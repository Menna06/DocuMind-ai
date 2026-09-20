"""ChromaDB vector store management."""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.config.settings import get_settings
from app.rag.embeddings import DocumentEmbedder


COLLECTION_NAME = "documind_documents"


class DocumentVectorStore:
    """Manage document chunks stored in ChromaDB."""

    def __init__(self) -> None:
        settings = get_settings()

        self.persist_directory = Path(settings.vectorstore_dir)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        self.embedder = DocumentEmbedder()

        self.store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=str(self.persist_directory),
            embedding_function=self.embedder.embeddings,
        )

    def add_documents(self, documents: list[Document]) -> list[str]:
        """Add document chunks to the vector store."""

        if not documents:
            return []

        return self.store.add_documents(documents)

    def count(self) -> int:
        """Return the number of stored document chunks."""

        return self.store._collection.count()

    def delete_document(self, filename: str) -> int:
        """Delete all document chunks associated with the specified filename.

        Args:
            filename: Name of the file whose chunks should be deleted.

        Returns:
            int: The number of deleted chunks.
        """
        if not filename:
            return 0

        safe_filename = Path(filename).name
        data = self.store._collection.get(include=["metadatas"])

        ids = data.get("ids") or []
        metadatas = data.get("metadatas") or []

        ids_to_delete = [
            doc_id
            for doc_id, meta in zip(ids, metadatas)
            if meta and Path(meta.get("source", "")).name == safe_filename
        ]

        if ids_to_delete:
            self.store.delete(ids=ids_to_delete)

        return len(ids_to_delete)
