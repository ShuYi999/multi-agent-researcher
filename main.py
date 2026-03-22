from dotenv import load_dotenv

load_dotenv(override=True)

from fastapi import FastAPI
from pydantic import BaseModel
from src.coordinator import Coordinator

app = FastAPI()
coordinator = Coordinator()


class ResearchRequest(BaseModel):
    question: str


class ResearchResponse(BaseModel):
    question: str
    raw_research: str
    report: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    result = coordinator.run(request.question)
    return ResearchResponse(**result)
