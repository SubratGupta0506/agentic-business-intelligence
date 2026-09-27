from app.tools.business_tools import analyze_business_data


def main():

    result = analyze_business_data(
        metric="profit",
        dimension="region"
    )

    print("\nAnalytics Tool Result:\n")

    for item in result["results"]:
        print(
            f"{item['name']}: "
            f"{item['value']}"
        )


if __name__ == "__main__":
    main()