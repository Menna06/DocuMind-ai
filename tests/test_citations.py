"""Tests for grounded evidence extraction and citation filtering (app.rag.citations)."""

from langchain_core.documents import Document

from app.rag.citations import (
    extract_evidence_sources,
    is_not_found_answer,
    _chunks_overlap,
    _tokenize,
)


class TestCitationsEvidenceExtraction:
    """Test suite for extract_evidence_sources."""

    def test_empty_documents_returns_empty(self) -> None:
        """Passing an empty document list should return an empty list."""
        assert extract_evidence_sources("Some answer", "Some query", []) == []

    def test_empty_answer_returns_first_documents(self) -> None:
        """If answer is empty, return initial documents up to max_sources."""
        docs = [
            Document(page_content="Doc 1", metadata={"source": "a.pdf", "page": 0}),
            Document(page_content="Doc 2", metadata={"source": "a.pdf", "page": 1}),
        ]
        result = extract_evidence_sources("", "query", docs, max_sources=1)
        assert len(result) == 1
        assert result[0].page_content == "Doc 1"

    def test_deduplicates_exact_content(self) -> None:
        """Duplicate chunks with identical content should be deduplicated to a single result."""
        docs = [
            Document(page_content="Duplicate chunk text", metadata={"source": "a.pdf", "page": 0}),
            Document(page_content="Duplicate chunk text", metadata={"source": "a.pdf", "page": 0}),
        ]
        result = extract_evidence_sources(
            "Duplicate chunk text answer",
            "query",
            docs,
        )
        assert len(result) == 1

    def test_filters_weak_irrelevant_chunks_for_specific_query(self) -> None:
        """When only one chunk provides the specific answer, weaker chunks should be excluded."""
        chunk_target = Document(
            page_content=(
                "The software implementation agreement signed on 14 February 2026 "
                "for deployment of Morrow's platform."
            ),
            metadata={"source": "contract.pdf", "page": 0},
        )
        chunk_weak = Document(
            page_content=(
                "Confidential Information included customer records, credentials, "
                "and technical documentation with administrative safeguards."
            ),
            metadata={"source": "contract.pdf", "page": 0},
        )
        chunk_other = Document(
            page_content="Vendor shall deliver warranty support for twelve months.",
            metadata={"source": "contract.pdf", "page": 1},
        )

        docs = [chunk_target, chunk_weak, chunk_other]
        result = extract_evidence_sources(
            answer="The software implementation agreement was signed on 14 February 2026.",
            query="When was software implementation agreement signed",
            documents=docs,
        )

        assert len(result) == 1
        assert result[0] == chunk_target

    def test_suppresses_overlapping_adjacent_chunks(self) -> None:
        """Adjacent chunks that overlap heavily due to sliding window should not both be returned."""
        shared_text = (
            "a software implementation agreement signed on 14 February 2026 for deployment "
            "of Morrow's inventory forecasting platform across Northstar's operations."
        )
        chunk_header = Document(
            page_content=f"CONFIDENTIAL COURT FILE Case No 123. Overview: {shared_text}",
            metadata={"source": "contract.pdf", "page": 0},
        )
        chunk_body = Document(
            page_content=f"{shared_text} The agreement required Northstar to pay USD 84,000.",
            metadata={"source": "contract.pdf", "page": 0},
        )

        result = extract_evidence_sources(
            answer="The software implementation agreement was signed on 14 February 2026.",
            query="When was software implementation agreement signed",
            documents=[chunk_header, chunk_body],
        )

        # Only one chunk should be retained because of the 100+ character overlap
        assert len(result) == 1

    def test_multi_topic_answer_retains_multiple_grounded_chunks(self) -> None:
        """When an answer draws on multiple distinct sections, all supporting chunks are retained."""
        chunk_date = Document(
            page_content="The agreement was signed on 14 February 2026.",
            metadata={"source": "contract.pdf", "page": 0},
        )
        chunk_fee = Document(
            page_content="The total implementation fee was USD 84,000 payable in three milestones.",
            metadata={"source": "contract.pdf", "page": 1},
        )

        docs = [chunk_date, chunk_fee]
        result = extract_evidence_sources(
            answer="The agreement was signed on 14 February 2026 and the total fee was USD 84,000.",
            query="When was the agreement signed and what was the fee?",
            documents=docs,
        )

        assert len(result) == 2
        assert chunk_date in result
        assert chunk_fee in result

    def test_chunks_overlap_helper(self) -> None:
        """_chunks_overlap should accurately detect substring matches >= min_chars."""
        t1 = "This is a unique test sequence that spans well over fifty characters for testing."
        t2 = "Prefix text... This is a unique test sequence that spans well over fifty characters for testing. Suffix text."
        assert _chunks_overlap(t1, t2, min_chars=40) is True
        assert _chunks_overlap("Short", "Another short", min_chars=50) is False

    def test_is_not_found_answer_detection(self) -> None:
        """Various expressions of absence of document information should be detected."""
        assert is_not_found_answer("The information is not available in the provided documents.") is True
        assert is_not_found_answer("The information about when Laylani grew up is not available in the provided documents.") is True
        assert is_not_found_answer("This information is not mentioned in the provided documents.") is True
        assert is_not_found_answer("The provided documents do not contain any information regarding this.") is True
        assert is_not_found_answer("I cannot find any information in the provided context.") is True
        assert is_not_found_answer("The contract was signed on 14 February 2026.") is False

    def test_unsupported_answer_returns_no_evidence(self) -> None:
        """When an answer states information is not available, zero evidence cards should be returned."""
        docs = [
            Document(page_content="Web Projects 2025 portfolio content...", metadata={"source": "Web Projects 2025.pdf", "page": 0}),
            Document(page_content="Court file agreement details...", metadata={"source": "DocuMind_Legal.pdf", "page": 0}),
        ]
        result = extract_evidence_sources(
            answer="The information is not available in the provided documents.",
            query="when did laylani grow up",
            documents=docs,
        )
        assert result == []

    def test_irrelevant_chunks_with_zero_score_returns_no_evidence(self) -> None:
        """When retrieved chunks share zero content with the answer, no evidence should be returned."""
        docs = [
            Document(page_content="Unrelated text about cooking and recipes.", metadata={"source": "recipes.pdf", "page": 0}),
            Document(page_content="Gardening tips for springtime flowers.", metadata={"source": "garden.pdf", "page": 1}),
        ]
        result = extract_evidence_sources(
            answer="Quantum computing utilizes qubits for superposition.",
            query="What is quantum computing?",
            documents=docs,
        )
        assert result == []
