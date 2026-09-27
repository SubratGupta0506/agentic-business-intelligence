import pandas as pd


INPUT_FILE = "data/superstore.csv"
OUTPUT_FILE = "data/superstore_cleaned.csv"


def clean_dataset():

    print("Loading dataset...")

    df = pd.read_csv(
        INPUT_FILE,
        encoding_errors="ignore"
    )

    print(f"Original shape: {df.shape}")

    # --------------------------------------------------
    # 1. Remove unnecessary / derived source columns
    # --------------------------------------------------

    columns_to_drop = [
        "记录数",
        "Year",
        "weeknum"
    ]

    df = df.drop(
        columns=columns_to_drop,
        errors="ignore"
    )

    # --------------------------------------------------
    # 2. Rename columns
    # --------------------------------------------------

    rename_map = {
        "Category": "category",
        "City": "city",
        "Country": "country",
        "Customer.ID": "customer_id",
        "Customer.Name": "customer_name",
        "Discount": "discount",
        "Market": "market",
        "Market2": "market_2",
        "Order.Date": "order_date",
        "Order.ID": "order_id",
        "Order.Priority": "order_priority",
        "Product.ID": "product_id",
        "Product.Name": "product_name",
        "Profit": "profit",
        "Quantity": "quantity",
        "Region": "region",
        "Row.ID": "row_id",
        "Sales": "sales",
        "Segment": "segment",
        "Ship.Date": "ship_date",
        "Ship.Mode": "ship_mode",
        "Shipping.Cost": "shipping_cost",
        "State": "state",
        "Sub.Category": "sub_category"
    }

    df = df.rename(
        columns=rename_map
    )

    # --------------------------------------------------
    # 3. Convert date columns
    # --------------------------------------------------

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    df["ship_date"] = pd.to_datetime(
        df["ship_date"],
        errors="coerce"
    )

    # --------------------------------------------------
    # 4. Check invalid dates
    # --------------------------------------------------

    invalid_order_dates = df["order_date"].isna().sum()
    invalid_ship_dates = df["ship_date"].isna().sum()

    print(f"Invalid order dates: {invalid_order_dates}")
    print(f"Invalid ship dates: {invalid_ship_dates}")

    # --------------------------------------------------
    # 5. Remove duplicate rows
    # --------------------------------------------------

    before = len(df)

    df = df.drop_duplicates(
        subset=["row_id"]
    )

    after = len(df)

    print(f"Duplicate rows removed: {before - after}")

    # --------------------------------------------------
    # 6. Ensure numeric columns have correct types
    # --------------------------------------------------

    numeric_columns = [
        "sales",
        "profit",
        "quantity",
        "discount",
        "shipping_cost"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # --------------------------------------------------
    # 7. Recalculate profit margin
    # --------------------------------------------------

    df["profit_margin"] = (
        df["profit"]
        .div(df["sales"].where(df["sales"] != 0))
        * 100
    )

    # --------------------------------------------------
    # 8. Check missing values
    # --------------------------------------------------

    print("\nMissing values after cleaning:")

    missing_values = df.isnull().sum()

    print(
        missing_values[
            missing_values > 0
        ]
    )

    # --------------------------------------------------
    # 9. Convert dates to YYYY-MM-DD
    # --------------------------------------------------

    df["order_date"] = df["order_date"].dt.strftime(
        "%Y-%m-%d"
    )

    df["ship_date"] = df["ship_date"].dt.strftime(
        "%Y-%m-%d"
    )

    # --------------------------------------------------
    # 10. Save final cleaned dataset
    # --------------------------------------------------

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nCleaning completed successfully.")

    print(
        f"Final shape: {df.shape}"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    clean_dataset()