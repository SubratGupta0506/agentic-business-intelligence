from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# 1. Define the state
class BusinessState(TypedDict):
    question: str
    result: str


# 2. Define a node
def analyze_question(state: BusinessState):
    question = state["question"]

    result = f"Received business question: {question}"

    return {
        "result": result
    }


# 3. Create the graph
builder = StateGraph(BusinessState)


# 4. Add the node
builder.add_node(
    "analyze_question",
    analyze_question
)


# 5. Connect START → node
builder.add_edge(
    START,
    "analyze_question"
)


# 6. Connect node → END
builder.add_edge(
    "analyze_question",
    END
)


# 7. Compile the graph
graph = builder.compile()


# 8. Run the graph
if __name__ == "__main__":

    initial_state = {
        "question": "Why did sales decline in July 2014?",
        "result": ""
    }

    final_state = graph.invoke(initial_state)

    print("Final State:")
    print(final_state)