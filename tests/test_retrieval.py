from app.graph import route_question
from app.retrieval import Document, retrieve


def test_retrieve_prefers_matching_document():
    docs = [
        Document("a", "Refund", "refund available within 30 days"),
        Document("b", "Security", "data encrypted at rest"),
    ]
    results = retrieve("refund policy", docs)
    assert results[0].document.id == "a"
    assert results[0].score > 0


def test_routes_policy_question():
    assert route_question("Can I get a refund?") == "policy_retrieval"


def test_routes_security_question():
    assert route_question("How is data encrypted?") == "security_retrieval"
