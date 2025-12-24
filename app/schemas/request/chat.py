from pydantic import BaseModel, Field


class Message(BaseModel):
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """
    聊天请求模型

    """
    chat_id: str = Field(..., description="聊天会话ID")
    message: Message = Field(..., description="用户消息")