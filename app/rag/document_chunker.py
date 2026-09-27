from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.document_loader import load_documents


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for document in documents:

        document_chunks = splitter.create_documents(
            [document["text"]]
        )

        for chunk in document_chunks:

            chunks.append({
                "source": document["source"],
                "text": chunk.page_content
            })

    return chunks


if __name__ == "__main__":

    documents = load_documents()

    chunks = chunk_documents(
        documents
    )

    print(
        f"Documents loaded: {len(documents)}"
    )

    print(
        f"Total chunks created: {len(chunks)}"
    )

    print("\nFirst 5 chunks:\n")

    for index, chunk in enumerate(chunks[:5]):

        print(
            f"Chunk {index + 1}"
        )

        print(
            f"Source: {chunk['source']}"
        )

        print(
            f"Characters: {len(chunk['text'])}"
        )

        print(
            chunk["text"][:500]
        )

        print(
            "=" * 70
        )