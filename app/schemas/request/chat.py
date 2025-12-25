from pydantic import BaseModel, Field


class Message(BaseModel):
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """
    聊天请求模型

    """
    session_id: str | None = Field(default=None, description="聊天会话ID")
    message: Message = Field(..., description="用户消息")
