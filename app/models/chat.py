from typing import Dict, Any

from sqlalchemy import String, Text, JSON, BIGINT, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class ChatSession(DeclarativeBase):
    """
    聊天会话表
    """
    __tablename__ = "chat_sessions"
    __table_args__ = {"comment": "聊天会话表"}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, sort_order=-1, comment="会话ID（UUID）")
    user_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False, comment="用户ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="会话标题")

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, comment="是否已删除,逻辑删除")

    created_at: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="记录创建时间,毫秒时间戳")
    updated_at: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="记录更新时间,毫秒时间戳")


class ChatMessage(DeclarativeBase):
    """
    聊天记录表
    """
    __tablename__ = "chat_messages"
    __table_args__ = {"comment": "聊天记录表"}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, sort_order=-1, comment="消息ID（UUID）")
    session_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False, comment="会话ID")
    type: Mapped[str] = mapped_column(String(20), nullable=False,
                                      comment="消息类型（system_message,human_message,ai_message,tool_message）")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="消息内容")
    meta_data: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=True, 
                                                      comment="元数据：包含引用(citations)、Token消耗(usage)、链路追踪ID(trace_id)等")

    created_at: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="记录创建时间,毫秒时间戳")
