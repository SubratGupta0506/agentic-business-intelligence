from app.tools.business_tools import analyze_profit_trend


def main():

    result = analyze_profit_trend()

    print("\nProfit Trend:\n")

    for item in result["results"]:

        print(
            f"{item['year']} | "
            f"Sales: {item['total_sales']:.2f} | "
            f"Profit: {item['total_profit']:.2f} | "
            f"Margin: {item['profit_margin']:.2f}%"
        )


if __name__ == "__main__":
    main()