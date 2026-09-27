from app.agents.business_agent import BusinessAgent


def main():

    agent = BusinessAgent()

    question = (
        "Sales declined in July 2014 compared with June 2014. "
        "What happened, and how should we interpret the role "
        "of discounting according to the company's business policies?"
    )

    response = agent.run(question)

    print("\nBusiness Investigation:\n")
    print(response)


if __name__ == "__main__":
    main()