"""Tests for document chunking."""

from langchain_core.documents import Document
import pytest

from app.rag.chunker import DocumentChunker


def test_documents_are_split_into_chunks() -> None:
    """A long document should be split into multiple chunks."""

    document = Document(
        page_content="This is a test document. " * 100,
        metadata={"source": "test.pdf", "page": 0},
    )

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.split_documents([document])

    assert len(chunks) > 1
    assert all(len(chunk.page_content) <= 100 for chunk in chunks)


def test_chunk_metadata_is_preserved() -> None:
    """Document metadata should be preserved on generated chunks."""

    document = Document(
        page_content="This is test content. " * 50,
        metadata={"source": "test.pdf", "page": 2},
    )

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.split_documents([document])

    assert chunks
    assert all(chunk.metadata["source"] == "test.pdf" for chunk in chunks)
    assert all(chunk.metadata["page"] == 2 for chunk in chunks)


def test_invalid_chunk_size_is_rejected() -> None:
    """A non-positive chunk size should raise an error."""

    with pytest.raises(ValueError, match="chunk_size"):
        DocumentChunker(chunk_size=0)


def test_invalid_chunk_overlap_is_rejected() -> None:
    """An overlap equal to or larger than the chunk size should raise an error."""

    with pytest.raises(ValueError, match="chunk_overlap"):
        DocumentChunker(
            chunk_size=100,
            chunk_overlap=100,
        )


def test_empty_document_list_returns_no_chunks() -> None:
    """An empty document list should return an empty chunk list."""

    chunker = DocumentChunker()

    chunks = chunker.split_documents([])

    assert chunks == []