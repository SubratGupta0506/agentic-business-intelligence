from app.tools.business_tools import compare_period_dimension


def main():

    result = compare_period_dimension(
        year=2014,
        month=7,
        dimension="product",
        metric="sales"
    )

    print("\nJune → July 2014 Product Sales Change:\n")

    for item in result["results"]:

        change = item["change_percent"]

        if change is not None:

            print(
                f"{item['name']}: "
                f"June={item['previous_value']:.2f}, "
                f"July={item['current_value']:.2f}, "
                f"Change={item['absolute_change']:.2f}, "
                f"{change:.2f}%"
            )

        else:

            print(
                f"{item['name']}: "
                f"June={item['previous_value']:.2f}, "
                f"July={item['current_value']:.2f}, "
                f"Change={item['absolute_change']:.2f}"
            )


if __name__ == "__main__":
    main()