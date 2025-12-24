from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from agent.tools.case import search_case
from core.config import settings


class LawAgentBuilder:
    """
    法律智能体构建器，用于构建法律智能体
    """

    def __init__(self, model_name: str = "gpt-4.1-mini"):
        self.model_name = model_name

    def build(self):
        """
        构建法律智能体
        :return: 法律智能体
        """
        law_agent = create_agent(
            model=ChatOpenAI(model=self.model_name,base_url=settings.OPENAI_API_BASE,api_key=settings.OPENAI_API_KEY),
            tools=[search_case],
            debug=False
        )
        return law_agent


law_agent = LawAgentBuilder().build()
