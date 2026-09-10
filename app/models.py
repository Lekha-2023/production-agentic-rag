from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)
    top_k: int = Field(default=5, ge=1, le=20)


class Citation(BaseModel):
    source_id: str
    title: str
    score: float
    excerpt: str


class AskResponse(BaseModel):
    answer: str
    route: str
    confidence: float
    citations: list[Citation]
