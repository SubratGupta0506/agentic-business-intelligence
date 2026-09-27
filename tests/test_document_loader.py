from app.rag.document_loader import load_documents


def main():

    documents = load_documents()

    print(
        f"\nTotal documents loaded: "
        f"{len(documents)}\n"
    )

    for document in documents:

        print(
            f"Document: {document['source']}"
        )

        print(
            f"Characters: "
            f"{len(document['text'])}"
        )

        print(
            f"Preview:\n"
            f"{document['text'][:200]}"
        )

        print("=" * 70)


if __name__ == "__main__":
    main()