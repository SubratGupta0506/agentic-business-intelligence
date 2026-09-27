from sentence_transformers import SentenceTransformer

from app.rag.document_loader import load_documents
from app.rag.document_chunker import chunk_documents


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(self):

        print(
            f"Loading embedding model: {MODEL_NAME}"
        )

        self.model = SentenceTransformer(
            MODEL_NAME
        )

    def encode(self, texts):

        return self.model.encode(
            texts,
            normalize_embeddings=True
        )


def create_embeddings():

    documents = load_documents()

    chunks = chunk_documents(
        documents
    )

    model = EmbeddingModel()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts
    )

    return chunks, embeddings


if __name__ == "__main__":

    chunks, embeddings = create_embeddings()

    print(
        f"\nTotal chunks: {len(chunks)}"
    )

    print(
        f"Embedding shape: {embeddings.shape}"
    )

    print(
        f"First embedding dimensions: "
        f"{len(embeddings[0])}"
    )