from app.tools.business_tools import compare_months


def main():

    result = compare_months(
        year=2014,
        month=7
    )

    print("\nMonth Comparison:\n")

    for item in result["months"]:

        print(
            f"{item['year']}-{item['month']:02d} | "
            f"Sales: {item['sales']:.2f} | "
            f"Profit: {item['profit']:.2f} | "
            f"Quantity: {item['quantity']} | "
            f"Shipping: {item['shipping_cost']:.2f}"
        )


if __name__ == "__main__":
    main()