from app.rag.rag_tool import RAGTool


def main():

    rag = RAGTool()

    query = (
        "What are the business rules "
        "for high discounts?"
    )

    result = rag.search(
        query=query,
        top_k=5
    )

    print("\nRAG Query:")
    print(query)

    print("\nRetrieved Evidence:\n")

    for index, item in enumerate(
        result["results"]
    ):

        print(
            f"Result {index + 1}"
        )

        print(
            f"Score: {item['score']:.4f}"
        )

        print(
            f"Source: {item['source']}"
        )

        print(
            f"Text:\n{item['text']}"
        )

        print("=" * 70)


if __name__ == "__main__":
    main()