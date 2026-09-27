from typing import TypedDict, Any

from google.genai import types

from langgraph.graph import StateGraph, START, END

from app.llm.client import GeminiClient
from app.tools.business_tools import (
    ANALYTICS_TOOL,
    analyze_business_data,
)


# --------------------------------------------------
# 1. Graph State
# --------------------------------------------------

class BusinessState(TypedDict):
    question: str
    tool_call: Any
    tool_result: Any
    final_answer: str


# --------------------------------------------------
# 2. Gemini Agent Node
# --------------------------------------------------

client = GeminiClient()


def agent_node(state: BusinessState):

    question = state["question"]

    print("\n[Agent Node]")
    print(f"Question: {question}")

    response = client.generate_with_tools(
        contents=question,
        tools=[ANALYTICS_TOOL]
    )

    # Gemini may request a tool
    if response.function_calls:

        function_call = response.function_calls[0]

        print("\nGemini requested a tool:")
        print(f"Tool: {function_call.name}")
        print(f"Arguments: {function_call.args}")

        return {
            "tool_call": {
                "name": function_call.name,
                "args": function_call.args,
            }
        }

    # Gemini may answer directly
    print("\nGemini answered without a tool.")

    return {
        "final_answer": response.text
    }


# --------------------------------------------------
# 3. Route after Agent
# --------------------------------------------------

def route_after_agent(state: BusinessState):

    if state.get("tool_call"):
        return "tool"

    return "end"


# --------------------------------------------------
# 4. Tool Node
# --------------------------------------------------

def tool_node(state: BusinessState):

    print("\n[Tool Node]")

    tool_call = state["tool_call"]

    name = tool_call["name"]
    args = tool_call["args"]

    print(f"Executing: {name}")
    print(f"Arguments: {args}")

    if name == "analyze_business_data":

        result = analyze_business_data(
            metric=args["metric"],
            dimension=args["dimension"]
        )

    else:
        raise ValueError(
            f"Unknown tool: {name}"
        )

    print("\nTool result:")
    print(result)

    return {
        "tool_result": result
    }


# --------------------------------------------------
# 5. Final Agent Node
# --------------------------------------------------

def final_agent_node(state: BusinessState):

    print("\n[Agent Node - Final]")

    question = state["question"]
    tool_result = state["tool_result"]

    prompt = f"""
You are a business intelligence analyst.

User question:
{question}

Business data retrieved from PostgreSQL:
{tool_result}

Answer the user's question using the retrieved data.

Do not invent information.
Clearly distinguish facts from interpretation.
"""

    response = client.generate(prompt)

    return {
        "final_answer": response
    }


# --------------------------------------------------
# 6. Build Graph
# --------------------------------------------------

builder = StateGraph(BusinessState)


builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tool",
    tool_node
)

builder.add_node(
    "final_agent",
    final_agent_node
)


# START → Agent

builder.add_edge(
    START,
    "agent"
)


# Agent → Tool OR END

builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tool": "tool",
        "end": END
    }
)


# Tool → Final Agent

builder.add_edge(
    "tool",
    "final_agent"
)


# Final Agent → END

builder.add_edge(
    "final_agent",
    END
)


graph = builder.compile()


# --------------------------------------------------
# 7. Test
# --------------------------------------------------

if __name__ == "__main__":

    initial_state = {
        "question": (
            "Show me the sales, profit and quantity "
            "by region."
        ),
        "tool_call": None,
        "tool_result": None,
        "final_answer": ""
    }

    final_state = graph.invoke(
        initial_state
    )

    print("\n================================")
    print("FINAL ANSWER")
    print("================================")

    print(
        final_state["final_answer"]
    )