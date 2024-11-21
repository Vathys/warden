from ..states import AgentState


class BaseAgent:
    def __init__(self):
        pass

    def invoke(self, state: AgentState) -> AgentState:
        pass
