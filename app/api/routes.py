from fastapi import APIRouter

from app.agents.langgraph_investigation_demo import graph


router = APIRouter(prefix="/api")


@router.get("/tools")
def get_tools():
    return {
        "tools": [
            "analyze_monthly_trend",
            "compare_months",
            "analyze_period_by_dimension",
            "analyze_operational_change",
            "search_business_documents",
        ]
    }


@router.post("/investigate")
def investigate(request: dict):

    question = request.get("question")

    if not question or not question.strip():
        return {
            "error": "Question is required."
        }

    initial_state = {
        "question": question,
        "conversation": [],
        "tool_results": [],
        "final_answer": "",
    }

    result = graph.invoke(initial_state)

    return {
        "question": question,
        "answer": result["final_answer"],
        "evidence": result.get("tool_results", []),
    }