from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    text: str


@dataclass(frozen=True)
class Result:
    document: Document
    score: float


def _terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def lexical_score(query: str, text: str) -> float:
    q = _terms(query)
    d = _terms(text)
    return len(q & d) / max(len(q), 1)


def retrieve(query: str, documents: list[Document], top_k: int = 5) -> list[Result]:
    scored = [Result(doc, lexical_score(query, doc.text)) for doc in documents]
    return sorted(scored, key=lambda x: (-x.score, x.document.id))[:top_k]


def reciprocal_rank_fusion(*ranked_lists: list[Result], k: int = 60) -> list[Result]:
    scores: dict[str, float] = {}
    docs: dict[str, Document] = {}
    for ranked in ranked_lists:
        for rank, result in enumerate(ranked, start=1):
            scores[result.document.id] = scores.get(result.document.id, 0.0) + 1 / (k + rank)
            docs[result.document.id] = result.document
    return [Result(docs[i], s) for i, s in sorted(scores.items(), key=lambda x: (-x[1], x[0]))]
