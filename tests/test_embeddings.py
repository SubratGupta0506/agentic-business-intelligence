from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"


def main():

    model = SentenceTransformer(
        MODEL_NAME
    )

    texts = [
        "Discounts above 20 percent require manager approval.",
        "High discounts need approval from a manager.",
        "The company uses different shipping modes."
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    similarity_1 = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    similarity_2 = cosine_similarity(
        [embeddings[0]],
        [embeddings[2]]
    )[0][0]

    print(
        f"\nSimilarity between related sentences: "
        f"{similarity_1:.4f}"
    )

    print(
        f"Similarity between unrelated sentences: "
        f"{similarity_2:.4f}"
    )


if __name__ == "__main__":
    main()