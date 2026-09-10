from fastapi import FastAPI
from .graph import answer
from .models import AskRequest, AskResponse

app = FastAPI(title="Production Agentic RAG", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return answer(request.question, request.top_k)
