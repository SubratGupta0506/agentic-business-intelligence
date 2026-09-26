from app.llm.client import GeminiClient


def main():
    llm = GeminiClient()

    prompt = """
    You are an AI assistant for a business decision intelligence system.

    Explain in two sentences what you would do if a business user asked:

    "Why did our sales decrease last quarter?"
    """

    response = llm.generate(prompt)

    print("\nGemini Response:\n")
    print(response)


if __name__ == "__main__":
    main()