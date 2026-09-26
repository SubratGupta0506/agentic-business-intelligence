import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.tools.business_tools import get_sales_summary


load_dotenv()


class GeminiClient:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)

    def ask_with_tool(self, question: str) -> str:

        tool = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="get_sales_summary",
                    description="Get sales summary for a specific business region.",
                    parameters=types.Schema(
                        type="OBJECT",
                        properties={
                            "region": types.Schema(
                                type="STRING",
                                description="Business region such as North, South, East or West."
                            )
                        },
                        required=["region"]
                    )
                )
            ]
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=types.GenerateContentConfig(
                tools=[tool]
            )
        )

        if not response.function_calls:
            return response.text

        function_call = response.function_calls[0]

        if function_call.name == "get_sales_summary":
            result = get_sales_summary(
                region=function_call.args["region"]
            )

            return str(result)

        return "Unknown tool requested."