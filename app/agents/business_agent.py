from google.genai import types

from app.llm.client import GeminiClient
from app.tools.business_tools import SALES_TOOL, get_sales_summary


class BusinessAgent:

    def __init__(self):
        self.llm = GeminiClient()

    def run(self, question: str) -> str:

        contents = [question]

        response = self.llm.generate_with_tools(
            contents=contents,
            tools=[SALES_TOOL]
        )

        while response.function_calls:

            # Add Gemini's tool request to the conversation
            contents.append(response.candidates[0].content)

            function_response_parts = []

            for function_call in response.function_calls:

                if function_call.name == "get_sales_summary":

                    result = get_sales_summary(
                        region=function_call.args["region"]
                    )

                    function_response_parts.append(
                        types.Part.from_function_response(
                            name=function_call.name,
                            response={"result": result}
                        )
                    )

            # Send tool result back to Gemini
            contents.append(
                types.Content(
                    role="user",
                    parts=function_response_parts
                )
            )

            # Ask Gemini to continue
            response = self.llm.generate_with_tools(
                contents=contents,
                tools=[SALES_TOOL]
            )

        return response.text