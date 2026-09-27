from typing import TypedDict, Any

from google.genai import types

from langgraph.graph import StateGraph, START, END

from app.llm.client import GeminiClient
from app.tools.business_tools import (
    ANALYTICS_TOOL,
    analyze_business_data,
)


# ==================================================
# 1. GRAPH STATE
# ==================================================

class BusinessState(TypedDict):
    question: str
    conversation: list
    tool_result: Any
    final_answer: str


# ==================================================
# 2. GEMINI CLIENT
# ==================================================

client = GeminiClient()


# ==================================================
# 3. AGENT NODE
# ==================================================

def agent_node(state: BusinessState):

    print("\n==============================")
    print("[AGENT NODE]")
    print("==============================")

    question = state["question"]
    conversation = state["conversation"]

    # ------------------------------------------------
    # FIRST AGENT CALL
    # ------------------------------------------------

    if not conversation:

        user_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=question
                )
            ]
        )

        conversation.append(user_message)

    # ------------------------------------------------
    # SEND COMPLETE CONVERSATION TO GEMINI
    # ------------------------------------------------

    response = client.generate_with_tools(
        contents=conversation,
        tools=[ANALYTICS_TOOL]
    )

    # ------------------------------------------------
    # GEMINI REQUESTED A TOOL
    # ------------------------------------------------

    if response.function_calls:

        function_call = response.function_calls[0]

        print("\nGemini requested a tool:")

        print(
            f"Tool: {function_call.name}"
        )

        print(
            f"Arguments: {function_call.args}"
        )

        # IMPORTANT:
        # Store Gemini's original model response.
        #
        # This contains the actual function_call part.

        conversation.append(
            response.candidates[0].content
        )

        return {
            "conversation": conversation
        }

    # ------------------------------------------------
    # GEMINI RETURNED FINAL ANSWER
    # ------------------------------------------------

    print("\nGemini produced final answer.")

    return {
        "conversation": conversation,
        "final_answer": response.text
    }


# ==================================================
# 4. TOOL NODE
# ==================================================

def tool_node(state: BusinessState):

    print("\n==============================")
    print("[TOOL NODE]")
    print("==============================")

    conversation = state["conversation"]

    # ------------------------------------------------
    # FIND THE MOST RECENT FUNCTION CALL
    # ------------------------------------------------

    function_call = None

    for content in reversed(conversation):

        if not hasattr(content, "parts"):
            continue

        for part in content.parts:

            if part.function_call:

                function_call = part.function_call
                break

        if function_call:
            break

    if function_call is None:

        raise ValueError(
            "No function call found in conversation."
        )

    name = function_call.name
    args = function_call.args

    print(
        f"Executing tool: {name}"
    )

    print(
        f"Arguments: {args}"
    )

    # ------------------------------------------------
    # EXECUTE REAL POSTGRESQL TOOL
    # ------------------------------------------------

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

    # ------------------------------------------------
    # CREATE FUNCTION RESPONSE
    # ------------------------------------------------

    function_response = types.Part.from_function_response(
        name=name,
        response={
            "result": result
        }
    )

    # ------------------------------------------------
    # ADD FUNCTION RESPONSE AS USER TURN
    # ------------------------------------------------

    conversation.append(
        types.Content(
            role="user",
            parts=[
                function_response
            ]
        )
    )

    return {
        "conversation": conversation,
        "tool_result": result
    }


# ==================================================
# 5. ROUTING
# ==================================================

def route_after_agent(state: BusinessState):

    if state.get("final_answer"):

        return "end"

    return "tool"


# ==================================================
# 6. BUILD LANGGRAPH
# ==================================================

builder = StateGraph(BusinessState)


builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tool",
    tool_node
)


# --------------------------------------------------
# START → AGENT
# --------------------------------------------------

builder.add_edge(
    START,
    "agent"
)


# --------------------------------------------------
# AGENT → TOOL OR END
# --------------------------------------------------

builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tool": "tool",
        "end": END
    }
)


# --------------------------------------------------
# TOOL → AGENT
# --------------------------------------------------

builder.add_edge(
    "tool",
    "agent"
)


# --------------------------------------------------
# COMPILE
# --------------------------------------------------

graph = builder.compile()


# ==================================================
# 7. TEST
# ==================================================

if __name__ == "__main__":

    initial_state = {
        "question": (
            "Show me the sales and profit by region."
        ),
        "conversation": [],
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