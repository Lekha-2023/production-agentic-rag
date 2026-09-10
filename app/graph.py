from .models import AskResponse, Citation
from .providers import DeterministicLLM, OpenAICompatibleLLM
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


def _provider():
    try:
        return OpenAICompatibleLLM()
    except RuntimeError:
        return DeterministicLLM()


def answer(question: str, top_k: int = 5) -> AskResponse:
    route = route_question(question)
    results = retrieve(question, DEMO_DOCS, top_k)
    grounded = [r for r in results if r.score > 0]
    if not grounded:
        return AskResponse(answer="I could not find supporting information in the indexed documents.", route=route, confidence=0.0, citations=[])

    citations = [Citation(source_id=r.document.id, title=r.document.title, score=round(r.score, 3), excerpt=r.document.text) for r in grounded]
    context = "\n".join(f"[{c.source_id}] {c.title}: {c.excerpt}" for c in citations)
    prompt = f"Answer only from the supplied context. Cite source IDs inline.\n\nContext:\n{context}\n\nQuestion: {question}"
    generated = _provider().generate("You are a grounded enterprise assistant. Never invent unsupported facts.", prompt)
    return AskResponse(answer=generated, route=route, confidence=round(min(0.99, grounded[0].score), 3), citations=citations)
