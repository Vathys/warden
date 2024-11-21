import functools
from typing import Dict, Optional

from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from .agents import BaseAgent
from .agents.supervisor import SupervisorAgent
from .logger import setup_logger
from .states import AgentState
from .utils import agent_node


class Assistant:
    def __init__(self, agents: Optional[Dict[str, BaseAgent]] = None):
        if agents is None:
            from .agents.archiver import ArchiveAgent
            from .agents.researcher import ResearcherAgent

            self.agents = {
                "Researcher": ResearcherAgent(),
                "Archiver": ArchiveAgent(),
            }
        else:
            self.agents = agents

        self.supervisor = SupervisorAgent(members=list(self.agents.keys()))

        self.logger = setup_logger("Warden")

        self.create_workflow()

    def create_workflow(self):
        self.workflow = StateGraph(AgentState)
        for agent_name, agent in self.agents.items():
            node = functools.partial(agent_node, agent=agent, name=agent_name)
            self.workflow.add_node(agent_name, node)

        self.workflow.add_node("Supervisor", self.supervisor)

        for agent_name in self.agents.keys():
            self.workflow.add_edge(agent_name, "Supervisor")

        conditional_map = {k: k for k in self.agents.keys()}
        conditional_map["FINISH"] = END
        self.workflow.add_conditional_edges(
            "Supervisor", lambda x: x["next"], conditional_map
        )
        self.workflow.add_edge("Supervisor", START)
        self.graph = self.workflow.compile()

    def addAgent(self, name: str, agent: BaseAgent):
        if name in self.agents:
            raise ValueError(f"Agent with name {name} already exists.")

        self.agents[name] = agent
        self.supervisor.addMembers([name])
        self.create_workflow()

    def removeAgent(self, name: str):
        if name not in self.agents:
            raise ValueError(f"Agent with name {name} does not exist.")

        del self.agents[name]
        self.supervisor.removeMembers([name])
        self.create_workflow()

    def __call__(self, prompt: str):
        for s in self.graph.stream({"messages": [HumanMessage(content=prompt)]}):
            if "__end__" not in s:
                self.logger.info(s)
                self.logger.info("---")


if __name__ == "__main__":
    from .agents.chatbot import ChatbotAgent

    agents = {
        "Chatbot": ChatbotAgent(),
    }
    assistant = Assistant(agents=agents)
    assistant("What is the capital of France?")
    assistant("Who is the president of the United States?")
