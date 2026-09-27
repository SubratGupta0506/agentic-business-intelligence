from app.tools.business_tools import analyze_period_by_dimension


def main():

    result = analyze_period_by_dimension(
        year=2014,
        month=7,
        dimension="region",
        metric="sales"
    )

    print("\nJuly 2014 Sales by Region:\n")

    for item in result["results"]:

        print(
            f"{item['name']}: "
            f"{item['value']:.2f}"
        )


if __name__ == "__main__":
    main()