from google.genai import types

from app.llm.client import GeminiClient

from app.tools.business_tools import (
    ANALYTICS_TOOL,
    PROFIT_TREND_TOOL,
    MONTHLY_TREND_TOOL,
    PERIOD_COMPARISON_TOOL,
    OPERATIONAL_TOOL,
    analyze_business_data,
    analyze_profit_trend,
    analyze_monthly_trend,
    compare_period_dimension,
    analyze_operational_change
)

from app.rag.rag_tool import (
    RAG_TOOL,
    RAGTool
)


SYSTEM_INSTRUCTION = """
You are a Business Decision Intelligence Agent.

Your job is to investigate business questions using:

1. Real transaction data from PostgreSQL.
2. Internal business knowledge from the RAG document system.

Rules:

1. Never invent business facts.

2. Use SQL/analytics tools whenever numerical
   transaction evidence is required.

3. Use the business document search tool when
   business policies, definitions, rules, investigation
   methodology, or organizational context are required.

4. For simple ranking questions, use the appropriate
   SQL/analytics tool.

5. For business knowledge questions, use the RAG tool.

6. For complex questions, you may need BOTH:
   - SQL evidence
   - RAG business context

7. Distinguish observations from explanations.

8. Treat transaction data as evidence of what happened.

9. Treat business documents as business context,
   policies, definitions, and analytical guidance.

10. Do not treat fictional/demo policy information
    as historical facts about the original dataset.

11. Only claim a cause when the available evidence
    supports it.

12. If the data does not establish a cause,
    clearly say so.

13. Give concise business explanations supported
    by evidence.

14. Never evaluate the effectiveness of a business strategy
    unless the available evidence directly supports that evaluation.

15. An observed relationship between two variables must not
    automatically be described as a causal relationship.

16. Do not infer management intent, strategy, campaign purpose,
    or business decisions from transaction data alone.

17. When a business document describes a policy, use it as
    contextual guidance. Do not assume that the historical
    transactions followed that policy unless the data proves it.

18. When evidence shows that two things occurred together,
    describe the relationship as "coincided with", "was associated
    with", or "was observed alongside" rather than claiming causation.

19. If the evidence cannot establish why something happened,
    explicitly state that the cause remains unknown.

For investigations, structure the final answer as:

What happened
Evidence
Business Context
Observed Relationships
Possible Explanations
Conclusion
Limitations
"""


class BusinessAgent:

    def __init__(self):

        self.llm = GeminiClient()

        self.rag = RAGTool()

        self.tools = [
            ANALYTICS_TOOL,
            PROFIT_TREND_TOOL,
            MONTHLY_TREND_TOOL,
            PERIOD_COMPARISON_TOOL,
            OPERATIONAL_TOOL,
            RAG_TOOL
        ]

    def execute_tool(
        self,
        function_call
    ):

        name = function_call.name
        args = function_call.args

        if name == "analyze_business_data":

            return analyze_business_data(
                metric=args["metric"],
                dimension=args["dimension"]
            )

        if name == "analyze_profit_trend":

            return analyze_profit_trend()

        if name == "analyze_monthly_trend":

            return analyze_monthly_trend(
                year=args["year"],
                month=args["month"]
            )

        if name == "compare_period_dimension":

            return compare_period_dimension(
                year=args["year"],
                month=args["month"],
                dimension=args["dimension"],
                metric=args["metric"]
            )

        if name == "analyze_operational_change":

            return analyze_operational_change(
                year=args["year"],
                month=args["month"]
            )

        if name == "search_business_documents":

            return self.rag.search(
                query=args["query"],
                top_k=args.get("top_k", 5)
            )

        return {
            "error": f"Unknown tool: {name}"
        }

    def run(
        self,
        question: str
    ) -> str:

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=SYSTEM_INSTRUCTION
                    ),
                    types.Part.from_text(
                        text=question
                    )
                ]
            )
        ]

        response = self.llm.generate_with_tools(
            contents=contents,
            tools=self.tools
        )

        while response.function_calls:

            contents.append(
                response.candidates[0].content
            )

            function_response_parts = []

            for function_call in response.function_calls:

                result = self.execute_tool(
                    function_call
                )

                function_response_parts.append(
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={
                            "result": result
                        }
                    )
                )

            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts
                )
            )

            response = self.llm.generate_with_tools(
                contents=contents,
                tools=self.tools
            )

        return response.text