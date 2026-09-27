from google.genai import types

from app.tools.database import get_connection


ALLOWED_METRICS = {
    "sales": "SUM(sales)",
    "profit": "SUM(profit)",
    "quantity": "SUM(quantity)",
    "shipping_cost": "SUM(shipping_cost)"
}


ALLOWED_DIMENSIONS = {
    "region": "region",
    "country": "country",
    "category": "category",
    "sub_category": "sub_category",
    "segment": "segment",
    "product": "product_name",
    "customer": "customer_name"
}


def analyze_business_data(
    metric: str,
    dimension: str
) -> dict:

    if metric not in ALLOWED_METRICS:
        return {
            "error": f"Unsupported metric: {metric}"
        }

    if dimension not in ALLOWED_DIMENSIONS:
        return {
            "error": f"Unsupported dimension: {dimension}"
        }

    metric_sql = ALLOWED_METRICS[metric]
    dimension_sql = ALLOWED_DIMENSIONS[dimension]

    query = f"""
        SELECT
            {dimension_sql} AS dimension,
            {metric_sql} AS value
        FROM business_transactions
        GROUP BY {dimension_sql}
        ORDER BY value DESC
        LIMIT 10;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(query)

            rows = cur.fetchall()

    return {
        "metric": metric,
        "dimension": dimension,
        "results": [
            {
                "name": row[0],
                "value": float(row[1])
            }
            for row in rows
        ]
    }
def analyze_profit_trend() -> dict:

    query = """
        SELECT
            EXTRACT(YEAR FROM order_date)::INTEGER AS year,
            SUM(sales) AS total_sales,
            SUM(profit) AS total_profit,
            SUM(profit) / NULLIF(SUM(sales), 0) * 100 AS profit_margin
        FROM business_transactions
        GROUP BY year
        ORDER BY year;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(query)

            rows = cur.fetchall()

    return {
        "analysis": "profit_trend",
        "results": [
            {
                "year": row[0],
                "total_sales": float(row[1]),
                "total_profit": float(row[2]),
                "profit_margin": (
                    float(row[3])
                    if row[3] is not None
                    else None
                )
            }
            for row in rows
        ]
    }
def analyze_monthly_trend(
    year: int,
    month: int
) -> dict:

    query = """
        SELECT
            SUM(sales) AS total_sales,
            SUM(profit) AS total_profit,
            SUM(quantity) AS total_quantity,
            SUM(shipping_cost) AS total_shipping_cost,
            SUM(profit) / NULLIF(SUM(sales), 0) * 100
                AS profit_margin
        FROM business_transactions
        WHERE EXTRACT(YEAR FROM order_date) = %s
          AND EXTRACT(MONTH FROM order_date) = %s;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                query,
                (year, month)
            )

            row = cur.fetchone()

    return {
        "year": year,
        "month": month,
        "sales": float(row[0]) if row[0] is not None else 0,
        "profit": float(row[1]) if row[1] is not None else 0,
        "quantity": int(row[2]) if row[2] is not None else 0,
        "shipping_cost": (
            float(row[3])
            if row[3] is not None
            else 0
        ),
        "profit_margin": (
            float(row[4])
            if row[4] is not None
            else None
        )
    }
def compare_months(
    year: int,
    month: int
) -> dict:

    query = """
        SELECT
            EXTRACT(YEAR FROM order_date)::INTEGER AS year,
            EXTRACT(MONTH FROM order_date)::INTEGER AS month,
            SUM(sales) AS total_sales,
            SUM(profit) AS total_profit,
            SUM(quantity) AS total_quantity,
            SUM(shipping_cost) AS total_shipping_cost
        FROM business_transactions
        WHERE order_date >=
              make_date(%s, %s, 1) - INTERVAL '1 month'
          AND order_date <
              make_date(%s, %s, 1) + INTERVAL '2 months'
        GROUP BY year, month
        ORDER BY year, month;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                query,
                (year, month, year, month)
            )

            rows = cur.fetchall()

    results = []

    for row in rows:

        results.append({
            "year": row[0],
            "month": row[1],
            "sales": float(row[2]),
            "profit": float(row[3]),
            "quantity": int(row[4]),
            "shipping_cost": float(row[5])
        })

    return {
        "target_year": year,
        "target_month": month,
        "months": results
    }
def analyze_period_by_dimension(
    year: int,
    month: int,
    dimension: str,
    metric: str
) -> dict:

    if metric not in ALLOWED_METRICS:
        return {
            "error": f"Unsupported metric: {metric}"
        }

    if dimension not in ALLOWED_DIMENSIONS:
        return {
            "error": f"Unsupported dimension: {dimension}"
        }

    metric_sql = ALLOWED_METRICS[metric]
    dimension_sql = ALLOWED_DIMENSIONS[dimension]

    query = f"""
        SELECT
            {dimension_sql} AS dimension,
            {metric_sql} AS value
        FROM business_transactions
        WHERE EXTRACT(YEAR FROM order_date) = %s
          AND EXTRACT(MONTH FROM order_date) = %s
        GROUP BY {dimension_sql}
        ORDER BY value DESC
        LIMIT 10;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                query,
                (year, month)
            )

            rows = cur.fetchall()

    return {
        "year": year,
        "month": month,
        "dimension": dimension,
        "metric": metric,
        "results": [
            {
                "name": row[0],
                "value": float(row[1])
            }
            for row in rows
        ]
    }  

def compare_period_dimension(
    year: int,
    month: int,
    dimension: str,
    metric: str
) -> dict:

    if metric not in ALLOWED_METRICS:
        return {
            "error": f"Unsupported metric: {metric}"
        }

    if dimension not in ALLOWED_DIMENSIONS:
        return {
            "error": f"Unsupported dimension: {dimension}"
        }

    metric_sql = ALLOWED_METRICS[metric]
    dimension_sql = ALLOWED_DIMENSIONS[dimension]

    query = f"""
        WITH current_period AS (
            SELECT
                {dimension_sql} AS dimension,
                {metric_sql} AS value
            FROM business_transactions
            WHERE EXTRACT(YEAR FROM order_date) = %s
              AND EXTRACT(MONTH FROM order_date) = %s
            GROUP BY {dimension_sql}
        ),

        previous_period AS (
            SELECT
                {dimension_sql} AS dimension,
                {metric_sql} AS value
            FROM business_transactions
            WHERE order_date >=
                  make_date(%s, %s, 1) - INTERVAL '1 month'
              AND order_date <
                  make_date(%s, %s, 1)
            GROUP BY {dimension_sql}
        )

        SELECT
            COALESCE(c.dimension, p.dimension) AS dimension,
            COALESCE(p.value, 0) AS previous_value,
            COALESCE(c.value, 0) AS current_value,
            COALESCE(c.value, 0)
                - COALESCE(p.value, 0) AS absolute_change
        FROM current_period c
        FULL OUTER JOIN previous_period p
            ON c.dimension = p.dimension
        ORDER BY absolute_change ASC
        LIMIT 10;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                query,
                (
                    year,
                    month,
                    year,
                    month,
                    year,
                    month
                )
            )

            rows = cur.fetchall()

    results = []

    for row in rows:

        previous_value = float(row[1])
        current_value = float(row[2])
        absolute_change = float(row[3])

        if previous_value != 0:

            change_percent = (
                absolute_change
                / previous_value
            ) * 100

        else:

            change_percent = None

        results.append({
            "name": row[0],
            "previous_value": previous_value,
            "current_value": current_value,
            "absolute_change": absolute_change,
            "change_percent": change_percent
        })

    return {
        "year": year,
        "month": month,
        "dimension": dimension,
        "metric": metric,
        "results": results
    } 
def analyze_operational_change(
    year: int,
    month: int
) -> dict:

    query = """
        WITH current_period AS (
            SELECT
                SUM(sales) AS sales,
                SUM(profit) AS profit,
                SUM(quantity) AS quantity,
                SUM(discount * sales) /
                    NULLIF(SUM(sales), 0) AS weighted_discount,
                SUM(shipping_cost) AS shipping_cost
            FROM business_transactions
            WHERE EXTRACT(YEAR FROM order_date) = %s
              AND EXTRACT(MONTH FROM order_date) = %s
        ),

        previous_period AS (
            SELECT
                SUM(sales) AS sales,
                SUM(profit) AS profit,
                SUM(quantity) AS quantity,
                SUM(discount * sales) /
                    NULLIF(SUM(sales), 0) AS weighted_discount,
                SUM(shipping_cost) AS shipping_cost
            FROM business_transactions
            WHERE order_date >=
                  make_date(%s, %s, 1) - INTERVAL '1 month'
              AND order_date <
                  make_date(%s, %s, 1)
        )

        SELECT
            p.sales,
            c.sales,
            p.profit,
            c.profit,
            p.quantity,
            c.quantity,
            p.weighted_discount,
            c.weighted_discount,
            p.shipping_cost,
            c.shipping_cost
        FROM previous_period p
        CROSS JOIN current_period c;
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                query,
                (
                    year,
                    month,
                    year,
                    month,
                    year,
                    month
                )
            )

            row = cur.fetchone()

    metrics = [
        ("sales", row[0], row[1]),
        ("profit", row[2], row[3]),
        ("quantity", row[4], row[5]),
        ("weighted_discount", row[6], row[7]),
        ("shipping_cost", row[8], row[9])
    ]

    results = []

    for name, previous, current in metrics:

        previous = float(previous or 0)
        current = float(current or 0)

        absolute_change = current - previous

        if previous != 0:
            change_percent = (
                absolute_change / previous
            ) * 100
        else:
            change_percent = None

        results.append({
            "metric": name,
            "previous_value": previous,
            "current_value": current,
            "absolute_change": absolute_change,
            "change_percent": change_percent
        })

    return {
        "year": year,
        "month": month,
        "results": results
    }

ANALYTICS_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_business_data",
            description=(
                "Analyze real business data from PostgreSQL. "
                "Use this tool when the user asks for comparisons "
                "or rankings involving sales, profit, quantity, "
                "or shipping cost across business dimensions."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "metric": types.Schema(
                        type="STRING",
                        description=(
                            "Metric to analyze: sales, profit, "
                            "quantity, or shipping_cost."
                        )
                    ),
                    "dimension": types.Schema(
                        type="STRING",
                        description=(
                            "Dimension to analyze: region, country, "
                            "category, sub_category, segment, "
                            "product, or customer."
                        )
                    )
                },
                required=[
                    "metric",
                    "dimension"
                ]
            )
        )
    ]
)
PROFIT_TREND_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_profit_trend",
            description=(
                "Analyze yearly sales, profit and average profit "
                "margin from the real business database. "
                "Use this when investigating whether profit or "
                "sales changed over time."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={}
            )
        )
    ]
)
MONTHLY_TREND_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_monthly_trend",
            description=(
                "Analyze sales, profit, quantity, shipping cost "
                "and profit margin for a specific month and year."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "year": types.Schema(
                        type="INTEGER",
                        description="The year to analyze."
                    ),
                    "month": types.Schema(
                        type="INTEGER",
                        description=(
                            "The month to analyze, from 1 to 12."
                        )
                    )
                },
                required=[
                    "year",
                    "month"
                ]
            )
        )
    ]
)
OPERATIONAL_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="analyze_operational_change",
            description=(
                "Compare sales, profit, quantity, weighted discount "
                "and shipping cost between the target month and "
                "the previous month. Use this when investigating "
                "why business performance changed."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "year": types.Schema(
                        type="INTEGER",
                        description="Target year."
                    ),
                    "month": types.Schema(
                        type="INTEGER",
                        description="Target month from 1 to 12."
                    )
                },
                required=["year", "month"]
            )
        )
    ]
)


PERIOD_COMPARISON_TOOL = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="compare_period_dimension",
            description=(
                "Compare the target month with the previous month "
                "across a business dimension. Useful for finding "
                "which regions, categories, products, customers, "
                "or other dimensions caused a change in sales, "
                "profit, quantity, or shipping cost."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "year": types.Schema(
                        type="INTEGER",
                        description="Target year."
                    ),
                    "month": types.Schema(
                        type="INTEGER",
                        description="Target month from 1 to 12."
                    ),
                    "dimension": types.Schema(
                        type="STRING",
                        description=(
                            "Dimension: region, country, category, "
                            "sub_category, segment, product, or customer."
                        )
                    ),
                    "metric": types.Schema(
                        type="STRING",
                        description=(
                            "Metric: sales, profit, quantity, "
                            "or shipping_cost."
                        )
                    )
                },
                required=[
                    "year",
                    "month",
                    "dimension",
                    "metric"
                ]
            )
        )
    ]
)