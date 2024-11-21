from . import BaseAgent


class ResearcherAgent(BaseAgent):
    """
    Agent with tools to read the wiki and perform web searches.
    """

    pass


if __name__ == "__main__":
    agent = ResearcherAgent()

    answer1 = agent.invoke({"messages": "What is the capital of France?"})
    print(answer1)

    answer2 = agent.invoke({"messages": "Who is Ayasedi?"})
    print(answer2)
