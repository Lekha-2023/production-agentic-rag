from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_citations():
    response = client.post("/v1/ask", json={"question": "What is the refund policy?"})
    assert response.status_code == 200
    body = response.json()
    assert body["citations"]
    assert body["route"] == "policy_retrieval"
