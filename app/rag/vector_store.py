import pickle
from pathlib import Path

import faiss
import numpy as np

from app.rag.embeddings import create_embeddings


VECTOR_STORE_DIR = Path("data/vector_store")
INDEX_PATH = VECTOR_STORE_DIR / "business_documents.index"
METADATA_PATH = VECTOR_STORE_DIR / "metadata.pkl"


class VectorStore:

    def __init__(self):
        self.index = None
        self.chunks = []

    def build(self, embeddings, chunks):
        embeddings = np.asarray(embeddings, dtype="float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        self.chunks = chunks

    def search(self, query_embedding, top_k=5):
        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            results.append({
                "score": float(score),
                "source": self.chunks[index]["source"],
                "text": self.chunks[index]["text"]
            })

        return results

    def save(self):
        VECTOR_STORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(INDEX_PATH)
        )

        with open(METADATA_PATH, "wb") as file:
            pickle.dump(
                self.chunks,
                file
            )

        print("Vector store saved successfully.")
        print(f"Index: {INDEX_PATH}")
        print(f"Metadata: {METADATA_PATH}")

    def load(self):
        self.index = faiss.read_index(
            str(INDEX_PATH)
        )

        with open(METADATA_PATH, "rb") as file:
            self.chunks = pickle.load(file)

        print("Vector store loaded successfully.")
        print(f"Total vectors: {self.index.ntotal}")
        print(f"Vector dimension: {self.index.d}")

    def exists(self):
        return (
            INDEX_PATH.exists()
            and METADATA_PATH.exists()
        )


def build_vector_store():

    store = VectorStore()

    if store.exists():
        store.load()
        return store

    print("No saved vector store found.")
    print("Building vector store for the first time...")

    chunks, embeddings = create_embeddings()

    store.build(
        embeddings=embeddings,
        chunks=chunks
    )

    store.save()

    return store


if __name__ == "__main__":

    store = build_vector_store()

    print()
    print("Vector store ready.")
    print(f"Total vectors: {store.index.ntotal}")
    print(f"Vector dimension: {store.index.d}")