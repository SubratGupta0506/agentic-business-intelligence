from sentence_transformers import SentenceTransformer

from app.rag.vector_store import build_vector_store


MODEL_NAME = "all-MiniLM-L6-v2"


def main():

    store = build_vector_store()

    model = SentenceTransformer(
        MODEL_NAME
    )

    query = (
        "What happens when a customer order "
        "has a very high discount?"
    )

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    results = store.search(
        query_embedding,
        top_k=5
    )

    print("\nQuery:")
    print(query)

    print("\nRetrieved Documents:\n")

    for index, result in enumerate(results):

        print(
            f"Result {index + 1}"
        )

        print(
            f"Score: {result['score']:.4f}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Text:\n{result['text'][:500]}"
        )

        print("=" * 70)


if __name__ == "__main__":
    main()