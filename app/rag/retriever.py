"""Diverse semantic retrieval from the vector store."""

from langchain_core.documents import Document

from app.config.settings import get_settings
from app.rag.vectorstore import DocumentVectorStore


class DocumentRetriever:
    """Retrieve relevant and diverse document chunks for a user query."""

    def __init__(self) -> None:
        self.vector_store = DocumentVectorStore()
        self.top_k = get_settings().retrieval_top_k

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[Document]:
        """Return relevant and diverse document chunks for a query."""

        if not query.strip():
            return []

        limit = top_k if top_k is not None else self.top_k

        if limit <= 0:
            return []

        fetch_k = max(limit * 4, 10)

        return self.vector_store.store.max_marginal_relevance_search(
            query,
            k=limit,
            fetch_k=fetch_k,
            lambda_mult=0.5,
        )