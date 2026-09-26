from app.llm.client import GeminiClient


def main():

    llm = GeminiClient()

    question = "What is business revenue?"

    response = llm.ask_with_tool(question)

    print("\nFinal Response:\n")
    print(response)


if __name__ == "__main__":
    main()