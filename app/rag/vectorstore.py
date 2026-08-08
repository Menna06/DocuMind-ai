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
        
