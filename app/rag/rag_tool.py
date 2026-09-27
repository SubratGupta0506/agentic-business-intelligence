from sentence_transformers import SentenceTransformer
from google.genai import types

from app.rag.vector_store import build_vector_store


MODEL_NAME = "all-MiniLM-L6-v2"


class RAGTool:

    def __init__(self):

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        self.store = build_vector_store()

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> dict:

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        results = self.store.search(
            query_embedding,
            top_k=top_k
        )

        return {
            "query": query,
            "results": results
        }


RAG_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_business_documents",
            description=(
                "Search the company's internal business "
                "documents for policies, business rules, "
                "KPI definitions, investigation guidance, "
                "customer strategy, product strategy, "
                "shipping policy, and business analysis "
                "guidance. Use this tool when the answer "
                "requires business knowledge that is not "
                "available directly from PostgreSQL data."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "query": types.Schema(
                        type="STRING",
                        description=(
                            "Natural language search query "
                            "describing the business knowledge "
                            "you need."
                        )
                    ),
                    "top_k": types.Schema(
                        type="INTEGER",
                        description=(
                            "Number of relevant document "
                            "chunks to retrieve."
                        )
                    )
                },
                required=[
                    "query"
                ]
            )
        )
    ]
)