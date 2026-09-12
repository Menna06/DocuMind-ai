"""Source citation formatting and evidence extraction for grounded responses."""

from __future__ import annotations

import re
from typing import Sequence

from langchain_core.documents import Document

_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "aren't", "as", "at", "be", "because", "been",
    "before", "being", "below", "between", "both", "but", "by", "can't",
    "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from",
    "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
    "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
    "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its",
    "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
    "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's",
    "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves",
}


def _tokenize(text: str) -> list[str]:
    """Extract lowercase alphabetic/numeric tokens excluding stopwords."""
    return [
        word.lower()
        for word in re.findall(r"\b\w+\b", text)
        if word.lower() not in _STOPWORDS and len(word) > 1
    ]


def _get_ngrams(tokens: list[str], n: int = 2) -> set[str]:
    """Generate n-gram strings from a list of tokens."""
    if len(tokens) < n:
        return set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def _chunks_overlap(t1: str, t2: str, min_chars: int = 50) -> bool:
    """Check whether two chunk texts share a continuous sequence of at least min_chars."""
    norm1 = " ".join(t1.split())
    norm2 = " ".join(t2.split())

    if min_chars > len(norm1) or min_chars > len(norm2):
        return False

    step = max(10, min_chars // 3)
    for i in range(0, len(norm1) - min_chars + 1, step):
        segment = norm1[i : i + min_chars]
        if segment in norm2:
            return True

    return False


_NOT_FOUND_PATTERNS = [
    r"not available in the (?:provided|given)?\s*(?:documents?|context)",
    r"not mentioned in the (?:provided|given)?\s*(?:documents?|context)",
    r"not found in the (?:provided|given)?\s*(?:documents?|context)",
    r"(?:do|does) not contain (?:any )?information",
    r"no information (?:is|was|about [^.]+?)?\s*(?:available|provided|found)",
    r"no mention of .* in the (?:provided|given)?\s*(?:documents?|context)",
    r"cannot (?:be found|find|locate) (?:any )?information",
    r"not provided in the (?:provided|given)?\s*(?:documents?|context)",
    r"information is not available",
    r"information about .* is not available",
    r"is not available in the provided documents",
]


def is_not_found_answer(answer: str) -> bool:
    """Check whether the generated answer indicates information is absent from documents."""
    clean = answer.strip()
    if not clean:
        return False
    return any(re.search(pat, clean, re.IGNORECASE) for pat in _NOT_FOUND_PATTERNS)


def extract_evidence_sources(
    answer: str,
    query: str,
    documents: Sequence[Document],
    max_sources: int = 3,
) -> list[Document]:
    """Extract and rank only unique, non-overlapping document chunks that provide genuine evidence."""
    if not documents:
        return []

    clean_answer = answer.strip()
    if not clean_answer:
        return list(documents[:max_sources])

    # If the answer explicitly states that the information is not in the documents,
    # no supporting evidence exists by definition.
    if is_not_found_answer(clean_answer):
        return []

    ans_tokens = _tokenize(clean_answer)
    ans_token_set = set(ans_tokens)
    ans_bigrams = _get_ngrams(ans_tokens, 2)
    q_token_set = set(_tokenize(query))

    scored_candidates: list[dict] = []
    seen_texts: set[str] = set()

    for idx, doc in enumerate(documents):
        norm_content = " ".join(doc.page_content.split())
        if not norm_content:
            continue

        # Deduplicate exact text
        text_signature = norm_content[:240]
        if text_signature in seen_texts:
            continue
        seen_texts.add(text_signature)

        doc_tokens = _tokenize(doc.page_content)
        doc_token_set = set(doc_tokens)
        doc_bigrams = _get_ngrams(doc_tokens, 2)

        ans_token_match = len(ans_token_set.intersection(doc_token_set))
        ans_bi_match = len(ans_bigrams.intersection(doc_bigrams))
        q_match = len(q_token_set.intersection(doc_token_set))

        # Weight exact multi-word bigram matches heavily, followed by answer tokens and query tokens
        score = (ans_token_match * 1.5) + (ans_bi_match * 3.0) + (q_match * 1.0)
        density = score / max(len(doc_tokens), 1)

        scored_candidates.append(
            {
                "score": score,
                "density": density,
                "ans_token_match": ans_token_match,
                "ans_bi_match": ans_bi_match,
                "doc": doc,
                "idx": idx,
            }
        )

    if not scored_candidates:
        return []

    # Sort descending by score, then density
    scored_candidates.sort(
        key=lambda item: (item["score"], item["density"]),
        reverse=True,
    )

    max_score = scored_candidates[0]["score"]
    if max_score <= 0.0:
        return []

    selected: list[Document] = []

    for item in scored_candidates:
        if item["score"] <= 0.0:
            continue

        # If the top chunk has strong evidence, exclude chunks with under 45% of top score
        if max_score >= 3.0 and item["score"] < (max_score * 0.45):
            continue

        # Evidence chunks must share content words or n-grams with the generated answer
        if item["ans_token_match"] == 0 and item["ans_bi_match"] == 0:
            continue

        doc = item["doc"]
        doc_text = doc.page_content.strip()

        # Suppress adjacent overlapping chunks from the same source document
        is_overlap = False
        for chosen in selected:
            if chosen.metadata.get("source") == doc.metadata.get("source"):
                if _chunks_overlap(doc_text, chosen.page_content.strip()):
                    is_overlap = True
                    break

        if not is_overlap:
            selected.append(doc)

        if len(selected) >= max_sources:
            break

    return selected
