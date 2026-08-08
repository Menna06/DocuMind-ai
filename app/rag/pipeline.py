"""RAG pipeline orchestration coordinating ingestion and query workflows."""

from dataclasses import dataclass

from langchain_core.documents import Document

from app.rag.llm import DocumentAnswerGenerator
from app.rag.retriever import DocumentRetriever


@dataclass(frozen=True)
class RetrievalResult:
    """Represent retrieved document context and its source documents."""

    context: str
    documents: list[Document]


@dataclass(frozen=True)
class RAGQueryResult:
    """Represent a generated answer and its supporting documents."""

    answer: str
    context: str
    documents: list[Document]


class RAGPipeline:
    """Coordinate document retrieval and answer generation."""

    def __init__(self) -> None:
        self.retriever = DocumentRetriever()
        self.answer_generator = DocumentAnswerGenerator()

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

    def query(self, question: str) -> RAGQueryResult:
        """Retrieve document context and generate a grounded answer."""

        retrieval = self.retrieve_context(question)

        answer = self.answer_generator.generate_answer(
            question,
            retrieval.context,
        )

        return RAGQueryResult(
            answer=answer,
            context=retrieval.context,
            documents=retrieval.documents,
        )