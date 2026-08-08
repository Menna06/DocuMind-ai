"""LLM answer generation from retrieved document context."""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from app.config.settings import get_settings


SYSTEM_PROMPT = """You answer questions using only the provided document context.

If the answer is not supported by the document context, say that the information is not available in the provided documents.

Do not invent facts, sources, or details that are not present in the context.
"""


class DocumentAnswerGenerator:
    """Generate grounded answers using retrieved document context."""

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.is_configured:
            raise ValueError(
                "OPENAI_API_KEY must be configured before generating answers."
            )

        self.model = ChatOpenAI(
            model=settings.openai_chat_model,
            api_key=settings.openai_api_key,
            temperature=0,
        )

    def generate_answer(self, question: str, context: str) -> str:
        """Generate an answer using only the supplied document context."""

        if not question.strip():
            return ""

        if not context.strip():
            return (
                "The information is not available in the provided documents."
            )

        response = self.model.invoke(
            [
                (
                    "system",
                    SYSTEM_PROMPT,
                ),
                (
                    "human",
                    f"Document context:\n\n{context}\n\n"
                    f"Question:\n\n{question}",
                ),
            ]
        )

        return response.content