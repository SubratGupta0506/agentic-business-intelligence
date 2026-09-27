from app.tools.business_tools import get_sales_summary


def main():

    result = get_sales_summary("South")

    print("\nDatabase Tool Result:\n")
    print(result)


if __name__ == "__main__":
    main()