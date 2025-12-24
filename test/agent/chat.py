from schemas.request import ChatRequest, Message
from services.chat import ChatService

ChatService().chat_stream(ChatRequest(chat_id="123", message=Message(content="你好")))
