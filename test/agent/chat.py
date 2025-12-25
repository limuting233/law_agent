from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from schemas.request.chat import ChatRequest, Message

# ChatService().chat_stream(ChatRequest(chat_id="123", message=Message(content="你好")))
h = AIMessage(content="你好,我是法律智能体")
print(h.__dict__)
# a ={'content': '你好', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': None}
# h1=HumanMessage(**a)
# print(h1.__dict__)
# load_dotenv(override=True)
# agent = create_agent(
#     model=ChatOpenAI(model="gpt-4.1-mini"),
#     system_prompt="你是一个法律智能体，你的任务是回答用户的法律问题",
#     checkpointer=InMemorySaver()
# )
# config = {"configurable": {"thread_id": "123"}}
# agent.invoke(
#     {
#         "messages": [HumanMessage(content="你是什么智能体")],
#     },
#     config=config)
# s = agent.get_state(config)
# print(s.values["messages"])
