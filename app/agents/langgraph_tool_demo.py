from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from app.tools.business_tools import analyze_monthly_trend


# --------------------------------------------------
# 1. Define the graph state
# --------------------------------------------------

class BusinessState(TypedDict):
    question: str
    tool_required: bool
    tool_result: Any
    final_answer: str


# --------------------------------------------------
# 2. Agent node
# --------------------------------------------------

def agent_node(state: BusinessState):

    question = state["question"]

    print("\n[Agent Node]")
    print(f"Question: {question}")

    # Temporary decision logic.
    # Gemini will replace this later.
    if "sales" in question.lower():

        print("Agent decided that a database tool is required.")

        return {
            "tool_required": True
        }

    print("Agent decided that no tool is required.")

    return {
        "tool_required": False,
        "final_answer": (
            f"I can answer this directly: {question}"
        )
    }


# --------------------------------------------------
# 3. Real PostgreSQL tool node
# --------------------------------------------------

def tool_node(state: BusinessState):

    print("\n[Tool Node]")
    print("Calling PostgreSQL business analytics tool...")

    result = analyze_monthly_trend(
        year=2014,
        month=7
    )

    print("PostgreSQL tool executed.")
    print(f"Tool result: {result}")

    return {
        "tool_result": result
    }


# --------------------------------------------------
# 4. Final agent node
# --------------------------------------------------

def final_agent_node(state: BusinessState):

    print("\n[Agent Node - Final]")

    result = state["tool_result"]

    answer = (
        "July 2014 business performance:\n"
        f"Sales: {result['sales']}\n"
        f"Profit: {result['profit']}\n"
        f"Quantity: {result['quantity']}\n"
        f"Shipping Cost: {result['shipping_cost']}\n"
        f"Profit Margin: {result['profit_margin']:.2f}%"
    )

    return {
        "final_answer": answer
    }


# --------------------------------------------------
# 5. Conditional routing
# --------------------------------------------------

def route_after_agent(state: BusinessState):

    if state["tool_required"]:
        return "tool"

    return "end"


# --------------------------------------------------
# 6. Build the graph
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


# Compile

graph = builder.compile()


# --------------------------------------------------
# 7. Run
# --------------------------------------------------

if __name__ == "__main__":

    initial_state = {
        "question": "What happened to sales in July 2014?",
        "tool_required": False,
        "tool_result": {},
        "final_answer": ""
    }

    final_state = graph.invoke(
        initial_state
    )

    print("\n==============================")
    print("FINAL ANSWER")
    print("==============================")

    print(
        final_state["final_answer"]
    )