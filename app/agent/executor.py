from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
# from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from loguru import logger

from agent.state import LawAgentState
from agent.tools.case import search_case
from core.config import settings
# from psycopg import Connection
from psycopg import AsyncConnection


class LawAgentBuilder:
    """
    法律智能体构建器，用于构建法律智能体
    """

    def __init__(self, model_name: str = "gpt-4.1-mini"):
        self.model_name = model_name

    async def build(self):
        """
        构建法律智能体
        :return: 法律智能体
        """
        logger.info("正在构建法律智能体...")
        checkpointer_db_url = f"postgresql://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOST}:{settings.POSTGRESQL_PORT}/{settings.POSTGRESQL_DB}?sslmode=disable"
        # with PostgresSaver.from_conn_string(checkpointer_db_url) as checkpointer:
        #     checkpointer.setup()
        #
        #     law_agent = create_agent(
        #         model=ChatOpenAI(model=self.model_name, base_url=settings.OPENAI_API_BASE,
        #                          api_key=settings.OPENAI_API_KEY),
        #         # tools=[search_case],
        #         checkpointer=checkpointer,
        #         system_prompt="你是一个法律智能体，你的任务是根据用户的问题，查询法律案例。",
        #         # state_schema=LawAgentState,
        #         debug=True
        #     )
        #     return law_agent

        # 1.创建连接池
        connection = await AsyncConnection.connect(checkpointer_db_url,autocommit=True)
        # 2.使用连接实例化checkpointer
        checkpointer = AsyncPostgresSaver(conn=connection)
        await checkpointer.setup()

        law_agent = create_agent(
            model=ChatOpenAI(model=self.model_name, base_url=settings.OPENAI_API_BASE,
                             api_key=settings.OPENAI_API_KEY),
            # tools=[search_case],
            # checkpointer=InMemorySaver(),
            checkpointer=checkpointer,
            system_prompt="你是一个法律智能体，你的任务是根据用户的问题，查询法律案例。",
            state_schema=LawAgentState,
            # debug=True
        )
        logger.info("法律智能体构建完成")
        return law_agent


# law_agent = LawAgentBuilder().build()
law_agent = None
