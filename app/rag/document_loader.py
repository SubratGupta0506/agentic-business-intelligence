from pathlib import Path


DOCUMENTS_DIR = Path("data/documents")


def load_documents():

    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.md"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(
        f"Loaded {len(documents)} documents.\n"
    )

    for document in documents:

        print(
            f"Source: {document['source']}"
        )

        print(
            f"Characters: {len(document['text'])}"
        )

        print("-" * 50)