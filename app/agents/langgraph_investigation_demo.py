from typing import TypedDict, Any
import json

from google.genai import types

from langgraph.graph import StateGraph, START, END

from app.llm.client import GeminiClient

from app.tools.business_tools import (
    analyze_monthly_trend,
    compare_months,
    analyze_period_by_dimension,
    analyze_operational_change,
)

from app.rag.rag_tool import RAGTool


# ============================================================
# 1. GRAPH STATE
# ============================================================

class BusinessState(TypedDict):
    question: str
    conversation: list
    tool_results: list
    final_answer: str


# ============================================================
# 2. CLIENTS
# ============================================================

client = GeminiClient()

rag = RAGTool()


# ============================================================
# 3. TOOL FUNCTIONS
# ============================================================

def monthly_trend_tool(
    year: int,
    month: int
):

    return analyze_monthly_trend(
        year=year,
        month=month
    )


def month_comparison_tool(
    year: int,
    month: int
):

    return compare_months(
        year=year,
        month=month
    )


def dimension_analysis_tool(
    year: int,
    month: int,
    dimension: str,
    metric: str
):

    return analyze_period_by_dimension(
        year=year,
        month=month,
        dimension=dimension,
        metric=metric
    )


def operational_analysis_tool(
    year: int,
    month: int
):

    return analyze_operational_change(
        year=year,
        month=month
    )


def business_document_search_tool(
    query: str,
    top_k: int = 5
):

    return rag.search(
        query=query,
        top_k=top_k
    )


# ============================================================
# 4. GEMINI TOOL DEFINITIONS
# ============================================================

MONTHLY_TREND_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_monthly_trend",
            description=(
                "Analyze business performance for a specific "
                "month. Returns sales, profit, quantity, "
                "shipping cost and profit margin."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "year": types.Schema(
                        type="INTEGER",
                        description="Year to analyze."
                    ),
                    "month": types.Schema(
                        type="INTEGER",
                        description="Month number from 1 to 12."
                    )
                },
                required=[
                    "year",
                    "month"
                ]
            )
        )
    ]
)


MONTH_COMPARISON_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="compare_months",
            description=(
                "Compare a target month with surrounding months. "
                "Useful for understanding changes in sales, profit, "
                "quantity and shipping cost."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "year": types.Schema(
                        type="INTEGER",
                        description="Target year."
                    ),
                    "month": types.Schema(
                        type="INTEGER",
                        description="Target month from 1 to 12."
                    )
                },
                required=[
                    "year",
                    "month"
                ]
            )
        )
    ]
)


DIMENSION_ANALYSIS_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_period_by_dimension",
            description=(
                "Break down a month's business metric by a "
                "business dimension such as region, category, "
                "sub_category, segment, product or customer."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "year": types.Schema(
                        type="INTEGER",
                        description="Year to analyze."
                    ),
                    "month": types.Schema(
                        type="INTEGER",
                        description="Month to analyze."
                    ),
                    "dimension": types.Schema(
                        type="STRING",
                        description=(
                            "Dimension such as region, category, "
                            "sub_category, segment, product or customer."
                        )
                    ),
                    "metric": types.Schema(
                        type="STRING",
                        description=(
                            "Metric such as sales, profit, "
                            "quantity or shipping_cost."
                        )
                    )
                },
                required=[
                    "year",
                    "month",
                    "dimension",
                    "metric"
                ]
            )
        )
    ]
)


OPERATIONAL_ANALYSIS_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_operational_change",
            description=(
                "Analyze operational changes for a target month "
                "compared with the previous month, including "
                "sales, profit, quantity, shipping cost and "
                "weighted discount."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "year": types.Schema(
                        type="INTEGER",
                        description="Target year."
                    ),
                    "month": types.Schema(
                        type="INTEGER",
                        description="Target month."
                    )
                },
                required=[
                    "year",
                    "month"
                ]
            )
        )
    ]
)


BUSINESS_DOCUMENT_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_business_documents",
            description=(
                "Search internal business documents for business "
                "policies, KPI definitions, discount rules, "
                "customer strategy, product strategy, shipping "
                "policies and investigation guidance."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "query": types.Schema(
                        type="STRING",
                        description=(
                            "Business knowledge to search for."
                        )
                    ),
                    "top_k": types.Schema(
                        type="INTEGER",
                        description=(
                            "Number of document chunks to retrieve."
                        )
                    )
                },
                required=[
                    "query"
                ]
            )
        )
    ]
)


ALL_TOOLS = [
    MONTHLY_TREND_TOOL,
    MONTH_COMPARISON_TOOL,
    DIMENSION_ANALYSIS_TOOL,
    OPERATIONAL_ANALYSIS_TOOL,
    BUSINESS_DOCUMENT_TOOL,
]


# ============================================================
# 5. TOOL EXECUTION
# ============================================================

def execute_tool(
    name: str,
    args: dict
):

    if name == "analyze_monthly_trend":

        return monthly_trend_tool(
            year=args["year"],
            month=args["month"]
        )

    elif name == "compare_months":

        return month_comparison_tool(
            year=args["year"],
            month=args["month"]
        )

    elif name == "analyze_period_by_dimension":

        return dimension_analysis_tool(
            year=args["year"],
            month=args["month"],
            dimension=args["dimension"],
            metric=args["metric"]
        )

    elif name == "analyze_operational_change":

        return operational_analysis_tool(
            year=args["year"],
            month=args["month"]
        )

    elif name == "search_business_documents":

        return business_document_search_tool(
            query=args["query"],
            top_k=args.get("top_k", 5)
        )

    else:

        raise ValueError(
            f"Unknown tool: {name}"
        )


# ============================================================
# 6. INVESTIGATION AGENT NODE
# ============================================================

def agent_node(state: BusinessState):

    print("\n==============================")
    print("[INVESTIGATION AGENT]")
    print("==============================")

    conversation = state["conversation"]

    investigation_instruction = """
You are an autonomous Business Decision Intelligence Agent.

Investigate the user's business question using the available
business tools.

IMPORTANT RULES:

1. For a WHY question, investigate autonomously.

2. Do NOT ask the user what dimension or tool to use next.

3. Continue investigating when additional evidence is useful.

4. You may call multiple tools across multiple turns.

5. Use PostgreSQL/analytics tools for numerical transaction
   evidence.

6. Use business-document search when policies, definitions,
   business rules, or investigation guidance are relevant.

7. NEVER invent a tool result.

8. NEVER claim that a tool was executed unless its result is
   actually present in the conversation.

9. NEVER invent numbers, regions, categories, segments,
   products, customers, discounts or other business facts.

10. Distinguish between:
    - observed facts
    - relationships in the data
    - possible explanations
    - unsupported assumptions

11. Do not claim causation unless the available evidence
    directly supports it.

12. If the evidence is insufficient to establish a cause,
    explicitly state that the cause remains uncertain.

13. Continue using tools until enough evidence has been
    collected to answer the question responsibly.

14. Once sufficient evidence exists, stop using tools.
"""

    # --------------------------------------------------------
    # FIRST USER MESSAGE
    # --------------------------------------------------------

    if not conversation:

        user_message = types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=(
                        investigation_instruction
                        + "\n\nUSER QUESTION:\n"
                        + state["question"]
                    )
                )
            ]
        )

        conversation.append(
            user_message
        )

    # --------------------------------------------------------
    # SUBSEQUENT CALLS
    # --------------------------------------------------------

    else:

        # Add a short reminder before the next reasoning turn.
        conversation.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=(
                            "Continue the investigation. "
                            "Use another tool if additional "
                            "evidence is needed. Do not invent "
                            "any evidence."
                        )
                    )
                ]
            )
        )

    # --------------------------------------------------------
    # CALL GEMINI
    # --------------------------------------------------------

    response = client.generate_with_tools(
        contents=conversation,
        tools=ALL_TOOLS
    )

    # --------------------------------------------------------
    # TOOL REQUEST
    # --------------------------------------------------------

    if response.function_calls:

        function_call = response.function_calls[0]

        print("\nGemini requested a tool:")

        print(
            f"Tool: {function_call.name}"
        )

        print(
            f"Arguments: {function_call.args}"
        )

        # Preserve exact Gemini model response.
        conversation.append(
            response.candidates[0].content
        )

        return {
            "conversation": conversation
        }

    # --------------------------------------------------------
    # INVESTIGATION FINISHED
    # --------------------------------------------------------

    print(
        "\nGemini decided that enough evidence "
        "has been collected."
    )

    return {
        "conversation": conversation
    }


# ============================================================
# 7. TOOL NODE
# ============================================================

def tool_node(state: BusinessState):

    print("\n==============================")
    print("[TOOL NODE]")
    print("==============================")

    conversation = state["conversation"]

    # --------------------------------------------------------
    # FIND MOST RECENT FUNCTION CALL
    # --------------------------------------------------------

    function_call = None

    for content in reversed(conversation):

        if not hasattr(
            content,
            "parts"
        ):
            continue

        for part in content.parts:

            if part.function_call:

                function_call = part.function_call
                break

        if function_call:
            break

    if function_call is None:

        raise ValueError(
            "No function call found."
        )

    name = function_call.name
    args = function_call.args

    print(
        f"Executing: {name}"
    )

    print(
        f"Arguments: {args}"
    )

    # --------------------------------------------------------
    # EXECUTE TOOL
    # --------------------------------------------------------

    result = execute_tool(
        name=name,
        args=args
    )

    print("\nTool result:")
    print(result)

    # --------------------------------------------------------
    # STORE EVIDENCE
    # --------------------------------------------------------

    tool_results = list(
        state.get(
            "tool_results",
            []
        )
    )

    tool_results.append(
        {
            "tool": name,
            "arguments": args,
            "result": result
        }
    )

    # --------------------------------------------------------
    # CREATE FUNCTION RESPONSE
    # --------------------------------------------------------

    function_response = (
        types.Part.from_function_response(
            name=name,
            response={
                "result": result
            }
        )
    )

    # --------------------------------------------------------
    # ADD TOOL RESULT AS USER TURN
    # --------------------------------------------------------

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
        "tool_results": tool_results
    }


# ============================================================
# 8. ROUTE AFTER AGENT
# ============================================================

def route_after_agent(
    state: BusinessState
):

    # If the conversation contains a new function call,
    # execute the tool.

    for content in reversed(
        state["conversation"]
    ):

        if not hasattr(
            content,
            "parts"
        ):
            continue

        for part in content.parts:

            if part.function_call:

                return "tool"

        break

    # Otherwise investigation is finished.

    return "finalizer"


# ============================================================
# 9. FINALIZER NODE
# ============================================================

def finalizer_node(
    state: BusinessState
):

    print("\n==============================")
    print("[FINALIZER]")
    print("==============================")

    tool_results = state.get(
        "tool_results",
        []
    )

    # --------------------------------------------------------
    # Convert collected evidence to JSON
    # --------------------------------------------------------

    evidence_json = json.dumps(
        tool_results,
        indent=2,
        default=str
    )

    finalizer_prompt = f"""
You are the final reporting component of a Business Decision
Intelligence System.

Answer the user's question using ONLY the collected evidence
provided below.

USER QUESTION:
{state["question"]}

COLLECTED TOOL EVIDENCE:
{evidence_json}

STRICT EVIDENCE RULES:

1. Use ONLY facts contained in COLLECTED TOOL EVIDENCE.

2. Do NOT invent additional tool calls.

3. Do NOT invent numbers.

4. Do NOT mention regions, categories, segments, products,
   customers or metrics unless they appear in the evidence.

5. Do NOT claim that evidence was collected if it is not
   present above.

6. Distinguish facts from interpretations.

7. If evidence shows a relationship but not causation, say
   that the relationship is observed and that causation is
   not established.

8. Do not blame market conditions, company strategy,
   campaigns, competitors or other external causes unless
   the collected evidence directly supports them.

9. If the evidence is insufficient to determine the cause,
   explicitly say so.

10. Do not ask the user what to investigate next.

Use this structure:

WHAT HAPPENED
- State the main observed change.

EVIDENCE
- Summarize the relevant numerical evidence.

OBSERVED PATTERNS
- Explain patterns that are directly supported by the data.

POSSIBLE EXPLANATIONS
- Only include explanations that can reasonably be inferred.
- Clearly label them as possible explanations.
- Do not present them as established causes.

CONCLUSION
- State what the evidence supports.
- State what it does not establish.

LIMITATIONS
- Mention important evidence that was not available.
"""

    response = client.generate(
        finalizer_prompt
    )

    print(
        "\nFinalizer generated evidence-grounded answer."
    )

    return {
        "final_answer": response
    }


# ============================================================
# 10. BUILD LANGGRAPH
# ============================================================

builder = StateGraph(
    BusinessState
)


builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tool",
    tool_node
)

builder.add_node(
    "finalizer",
    finalizer_node
)


# ------------------------------------------------------------
# START → AGENT
# ------------------------------------------------------------

builder.add_edge(
    START,
    "agent"
)


# ------------------------------------------------------------
# AGENT → TOOL OR FINALIZER
# ------------------------------------------------------------

builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tool": "tool",
        "finalizer": "finalizer"
    }
)


# ------------------------------------------------------------
# TOOL → AGENT
# ------------------------------------------------------------

builder.add_edge(
    "tool",
    "agent"
)


# ------------------------------------------------------------
# FINALIZER → END
# ------------------------------------------------------------

builder.add_edge(
    "finalizer",
    END
)


# ------------------------------------------------------------
# COMPILE
# ------------------------------------------------------------

graph = builder.compile()


# ============================================================
# 11. TEST
# ============================================================

if __name__ == "__main__":

    initial_state = {
        "question": (
            "Why did sales decline in July 2014 "
            "compared with June 2014?"
        ),
        "conversation": [],
        "tool_results": [],
        "final_answer": ""
    }

    final_state = graph.invoke(
        initial_state
    )

    print("\n================================")
    print("FINAL BUSINESS INVESTIGATION")
    print("================================")

    print(
        final_state["final_answer"]
    )