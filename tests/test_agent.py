from app.agents.business_agent import BusinessAgent


def main():

    agent = BusinessAgent()

    question = "Which region has the highest sales?"

    response = agent.run(question)

    print("\nAgent Response:\n")
    print(response)


if __name__ == "__main__":
    main()