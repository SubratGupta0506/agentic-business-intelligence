from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.business_agent import BusinessAgent


app = FastAPI(
    title="Agentic Business Decision Intelligence System"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Agentic Business Decision Intelligence System is running"
    }


@app.post("/api/ask")
def ask_question(request: QuestionRequest):

    agent = BusinessAgent()

    response = agent.run(request.question)

    return {
        "question": request.question,
        "response": response
    }