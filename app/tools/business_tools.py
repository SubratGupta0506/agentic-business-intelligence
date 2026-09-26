from google.genai import types


def get_sales_summary(region: str) -> dict:
    sales_data = {
        "North": 120000,
        "South": 95000,
        "East": 80000,
        "West": 110000
    }

    sales = sales_data.get(region)

    if sales is None:
        return {
            "region": region,
            "error": "Region not found"
        }

    return {
        "region": region,
        "sales": sales
    }


SALES_TOOL = types.Tool(
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