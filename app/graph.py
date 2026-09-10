from .models import AskResponse, Citation
from .retrieval import Document, retrieve


DEMO_DOCS = [
    Document("refund-001", "Refund Policy", "Customers may request a refund within 30 days of purchase. Refunds are processed to the original payment method."),
    Document("security-001", "Security Policy", "Production data is encrypted in transit and at rest. Access follows least-privilege controls."),
    Document("support-001", "Support Guide", "Support requests are prioritized by severity. Critical incidents are escalated to the on-call engineer."),
]


def route_question(question: str) -> str:
    q = question.lower()
    if any(word in q for word in ("refund", "return", "money back")):
        return "policy_retrieval"
    if any(word in q for word in ("security", "encrypt", "access")):
        return "security_retrieval"
    return "general_retrieval"


def answer(question: str, top_k: int = 5) -> AskResponse:
    route = route_question(question)
    results = retrieve(question, DEMO_DOCS, top_k)
    grounded = [r for r in results if r.score > 0]
    if not grounded:
        return AskResponse(
            answer="I could not find supporting information in the indexed documents.",
            route=route,
            confidence=0.0,
            citations=[],
        )

    best = grounded[0]
    answer_text = f"Based on {best.document.title}: {best.document.text}"
    citations = [
        Citation(source_id=r.document.id, title=r.document.title, score=round(r.score, 3), excerpt=r.document.text)
        for r in grounded
    ]
    return AskResponse(
        answer=answer_text,
        route=route,
        confidence=round(min(0.99, best.score), 3),
        citations=citations,
    )
