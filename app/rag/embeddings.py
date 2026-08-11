"""Embedding generation for document chunks."""

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from app.config.settings import get_settings


class DocumentEmbedder:
    """Generate embeddings for document chunks."""

    def __init__(self) -> None:
        settings = get_settings()

        if settings.embedding_provider == "gemini":
            if not settings.gemini_api_key.strip():
                raise ValueError(
                    "GEMINI_API_KEY must be configured "
                    "before generating embeddings."
                )

            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=settings.gemini_embedding_model,
                google_api_key=settings.gemini_api_key,
            )

        elif settings.embedding_provider == "openai":
            if not settings.openai_api_key.strip():
                raise ValueError(
                    "OPENAI_API_KEY must be configured "
                    "before generating embeddings."
                )

            self.embeddings = OpenAIEmbeddings(
                model=settings.openai_embedding_model,
                api_key=settings.openai_api_key,
            )

        else:
            raise ValueError(
                f"Unsupported embedding provider: "
                f"{settings.embedding_provider}"
            )

    def embed_documents(
        self,
        documents: list[Document],
    ) -> list[list[float]]:
        """Generate embeddings for a list of document chunks."""

        if not documents:
            return []

        texts = [document.page_content for document in documents]

        return self.embeddings.embed_documents(texts)