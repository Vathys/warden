from langchain_core.messages import HumanMessage

from .agents import BaseAgent
from .states import AgentState


def agent_node(state: AgentState, agent: BaseAgent, name: str) -> AgentState:
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }
