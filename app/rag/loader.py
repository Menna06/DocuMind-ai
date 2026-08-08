"""PDF document loading using LangChain PyPDFLoader."""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFDocumentLoader:
    """Load PDF files into LangChain documents."""

    def load(self, file_path: Path) -> list[Document]:
        """Load a PDF and return its pages as LangChain documents."""

        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        if file_path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are supported.")

        loader = PyPDFLoader(str(file_path))
        return loader.load()
