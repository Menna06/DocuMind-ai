"""LLM answer generation from retrieved document context."""

from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI
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

        if settings.llm_provider == "gemini":
            if not settings.gemini_api_key.strip():
                raise ValueError(
                    "GEMINI_API_KEY must be configured "
                    "before generating answers."
                )

            self.model = ChatGoogleGenerativeAI(
                model=settings.gemini_chat_model,
                google_api_key=settings.gemini_api_key,
            )

        elif settings.llm_provider == "openai":
            if not settings.openai_api_key.strip():
                raise ValueError(
                    "OPENAI_API_KEY must be configured "
                    "before generating answers."
                )

            self.model = ChatOpenAI(
                model=settings.openai_chat_model,
                api_key=settings.openai_api_key,
                temperature=0,
            )

        else:
            raise ValueError(
                f"Unsupported LLM provider: {settings.llm_provider}"
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

        return self._extract_response_text(response.content)

    @staticmethod
    def _extract_response_text(content: object) -> str:
        """Normalize Gemini/OpenAI response content into plain text."""

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts: list[str] = []

            for block in content:
                if isinstance(block, dict):
                    text = block.get("text")
                    if isinstance(text, str):
                        text_parts.append(text)
                elif isinstance(block, str):
                    text_parts.append(block)

            return "\n".join(text_parts).strip()

        return str(content)