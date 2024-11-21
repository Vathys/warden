from . import BaseAgent


class ChatbotAgent(BaseAgent):
    """
    Agent that can respond to user queries.
    """

    pass


if __name__ == "__main__":
    agent = ChatbotAgent()

    answer1 = agent.invoke({"messages": "What is the capital of France?"})
    print(answer1)

    answer2 = agent.invoke({"messages": "What is the capital of Italy?"})
    print(answer2)
