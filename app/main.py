from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agents.business_agent import BusinessAgent


app = FastAPI(
    title="Agentic Business Decision Intelligence System"
)


# --------------------------------------------------
# CORS
# Allows the React frontend to communicate
# with the FastAPI backend during local development.
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Agentic Business Decision Intelligence System is running"
    }


# --------------------------------------------------
# Ask Business Question
# --------------------------------------------------

@app.post("/api/ask")
def ask_question(request: QuestionRequest):

    agent = BusinessAgent()

    response = agent.run(request.question)

    return {
        "question": request.question,
        "response": response
    }