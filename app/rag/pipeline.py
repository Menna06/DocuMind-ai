"""RAG pipeline orchestration coordinating ingestion and query workflows."""

from dataclasses import dataclass

from langchain_core.documents import Document

from app.rag.retriever import DocumentRetriever


@dataclass(frozen=True)
class RetrievalResult:
    """Represent retrieved document context and its source documents."""

    context: str
    documents: list[Document]


class RAGPipeline:
    """Coordinate document retrieval and context preparation."""

    def __init__(self) -> None:
        self.retriever = DocumentRetriever()

    def retrieve_context(self, query: str) -> RetrievalResult:
        """Retrieve relevant documents and prepare their text as context."""

        documents = self.retriever.retrieve(query)

        if not documents:
            return RetrievalResult(
                context="",
                documents=[],
            )

        context_parts = [
            document.page_content.strip()
            for document in documents
            if document.page_content.strip()
        ]

        return RetrievalResult(
            context="\n\n".join(context_parts),
            documents=documents,
        )