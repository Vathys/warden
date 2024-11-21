from typing import List, Literal

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from pydantic import BaseModel

from . import BaseAgent


class SupervisorAgent(BaseAgent):
    """
    Supervisor agent that manages a conversation between other agents.
    """

    def __init__(self, model="llama3.1", members=None, model_kwargs={}):
        self.llm = ChatOllama(model=model, **model_kwargs)

        self.system_prompt = (
            "You are a supervisor tasked with managing a conversation between the"
            " following workers: {members}. Given the following user request,"
            " respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status. When finished,"
            " respond with FINISH."
        )

        if members is None:
            self.members = ["Researcher", "Archiver"]
        else:
            self.members = members

        self.updatePrompt()

    def updatePrompt(self):
        options = ["FINISH"] + self.members
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    (
                        "Given the conversation above, who should act next?"
                        " Or should we FINISH? Select one of: {options}."
                    ),
                ),
            ]
        ).partial(options=str(options), members=", ".join(self.members))

    def addMembers(self, members: List[str]):
        self.members += members
        self.updatePrompt()

    def removeMembers(self, members: List[str]):
        for member in members:
            self.members.remove(member)
        self.updatePrompt()

    def getRouteResponse(self):
        options = ["FINISH"] + self.members

        class RouteResponse(BaseModel):
            next: Literal[*options]  # type: ignore

        return RouteResponse

    def invoke(self, state):
        supervisor_chain = self.prompt | self.llm.with_structured_output(
            self.getRouteResponse()
        )
        return supervisor_chain.invoke(state)

    def __call__(self, state):
        return self.invoke(state)
