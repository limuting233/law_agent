from typing import Literal, Any, Optional, Union

from pydantic import BaseModel, Field


class BaseMeta(BaseModel):
    """
    流式响应元数据基类
    """
    chat_id: str = Field(..., description="聊天会话ID")
    # trace_id: Optional[str] = Field(..., description="langchain跟踪ID")
    timestamp: int = Field(..., description="事件发生时间戳（毫秒级）")

class WorkflowStartMeta(BaseMeta):
    """
    工作流开始事件元数据
    """


class TextChunkMeta(BaseMeta):
    """
    文本块元数据
    """
    index: int = Field(..., description="文本块索引")
    # node: str = Field(..., description="当前处理节点")
    # model: str = Field(..., description="当前使用的模型")


class ToolUseMeta(BaseMeta):
    """
    工具调用元数据
    """
    # tool_id: str = Field(..., description="工具ID")
    # tool_call_id: str = Field(..., description="工具调用ID")
    tool_name: str = Field(..., description="工具名称")
    # tool_content: str = Field(..., description="工具的返回内容")
    # node: str = Field(..., description="当前处理节点")


class DoneMeta(BaseMeta):
    """
    完成事件元数据
    """


class ErrorMeta(BaseMeta):
    """
    错误事件元数据
    """
    code: int = Field(..., description="错误码")
    error_message: str = Field(..., description="错误信息")


class StreamResponse(BaseModel):
    """
    流式响应模型
    """
    event: Literal["workflow_start", "reasoning", "tool_use", "citation", "text_chunk", "error", "done"] = Field(...,
                                                                                                                 description="事件类型")
    data: Any = Field(..., description="事件数据")
    meta: Union[WorkflowStartMeta, TextChunkMeta, ToolUseMeta, DoneMeta, ErrorMeta] = Field(default=None, description="事件元数据")
