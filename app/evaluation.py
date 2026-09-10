from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    retrieval_hit: bool
    citation_coverage: float
    answer_grounded: bool


def evaluate(expected_source: str, cited_sources: list[str], answer: str, source_text: str) -> Evaluation:
    hit = expected_source in cited_sources
    coverage = 1.0 if cited_sources else 0.0
    grounded = bool(answer.strip()) and source_text.lower()[:40] in answer.lower()
    return Evaluation(hit, coverage, grounded)
