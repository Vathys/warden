from . import BaseAgent


class ArchiveAgent(BaseAgent):
    """
    Agent with tools to change the wiki. Is not responsible for reading the wiki.
    """

    pass


if __name__ == "__main__":
    agent = ArchiveAgent()

    answer1 = agent.invoke(
        {"messages": "Write 'This is a very important test' in the file 'test.txt'."}
    )
    print(answer1)

    answer2 = agent.invoke(
        {
            "messages": "Write 'This is another very important test' in the file 'test4.txt'"
        }
    )
    print(answer2)
