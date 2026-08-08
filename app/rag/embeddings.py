"""OpenAI embedding generation for document chunks."""

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.config.settings import get_settings


class DocumentEmbedder:
    """Generate embeddings for document chunks."""

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.is_configured:
            raise ValueError(
                "OPENAI_API_KEY must be configured before generating embeddings."
            )

        self.embeddings = OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            api_key=settings.openai_api_key,
        )

    def embed_documents(self, documents: list[Document]) -> list[list[float]]:
        """Generate embeddings for a list of document chunks."""

        if not documents:
            return []

        texts = [document.page_content for document in documents]

        return self.embeddings.embed_documents(texts)