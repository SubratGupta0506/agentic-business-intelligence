import pandas as pd
import psycopg


CSV_FILE = "data/superstore_cleaned.csv"

DB_CONFIG = {
    "dbname": "business_intelligence",
    "user": "postgres",
    "password": "YOUR_POSTGRES_PASSWORD",
    "host": "localhost",
    "port": 5432
}


def load_data():

    print("Loading cleaned dataset...")

    df = pd.read_csv(CSV_FILE)

    print(f"Rows to load: {len(df)}")

    with psycopg.connect(**DB_CONFIG) as conn:

        with conn.cursor() as cur:

            print("Connected to PostgreSQL.")

            insert_query = """
                INSERT INTO business_transactions (
                    row_id,
                    order_id,
                    order_date,
                    ship_date,
                    customer_id,
                    customer_name,
                    segment,
                    product_id,
                    product_name,
                    category,
                    sub_category,
                    country,
                    market,
                    market_2,
                    region,
                    state,
                    city,
                    sales,
                    profit,
                    quantity,
                    discount,
                    shipping_cost,
                    profit_margin,
                    ship_mode,
                    order_priority
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """

            records = df[
                [
                    "row_id",
                    "order_id",
                    "order_date",
                    "ship_date",
                    "customer_id",
                    "customer_name",
                    "segment",
                    "product_id",
                    "product_name",
                    "category",
                    "sub_category",
                    "country",
                    "market",
                    "market_2",
                    "region",
                    "state",
                    "city",
                    "sales",
                    "profit",
                    "quantity",
                    "discount",
                    "shipping_cost",
                    "profit_margin",
                    "ship_mode",
                    "order_priority"
                ]
            ].where(pd.notna(df), None)

            cur.executemany(
                insert_query,
                records.itertuples(index=False, name=None)
            )

        conn.commit()

    print("Data loaded successfully.")


if __name__ == "__main__":
    load_data()