from langchain.agents import AgentState
from pydantic import Field


class LawAgentState(AgentState):
    """
    法律智能体状态类，继承自AgentState，用于存储法律智能体的状态
    """
    user_id: str
