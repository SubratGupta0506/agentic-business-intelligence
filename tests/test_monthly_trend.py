from app.tools.business_tools import analyze_monthly_trend


def main():

    result = analyze_monthly_trend(
        year=2014,
        month=7
    )

    print("\nJuly 2014 Analysis:\n")

    print(
        f"Sales: {result['sales']:.2f}"
    )

    print(
        f"Profit: {result['profit']:.2f}"
    )

    print(
        f"Quantity: {result['quantity']}"
    )

    print(
        f"Shipping Cost: "
        f"{result['shipping_cost']:.2f}"
    )

    print(
        f"Profit Margin: "
        f"{result['profit_margin']:.2f}%"
    )


if __name__ == "__main__":
    main()