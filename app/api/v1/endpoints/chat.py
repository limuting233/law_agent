from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api import deps
from core.exceptions import BusinessException
from core.status_code import AppStatus
from core.stream_utils import sse_generator
from schemas.request.chat import ChatRequest
from services.chat import ChatService

router = APIRouter()

chat_service = ChatService()


@router.post("/stream")
async def stream_chat(request: ChatRequest, db: AsyncSession = Depends(deps.get_db)):
    """
    流式聊天接口
    :param request: 聊天请求模型
    :param db: 异步数据库会话, 依赖注入
    :return: 流式响应
    """

    return StreamingResponse(
        content=sse_generator(chat_service.chat_stream(request)),
        media_type="text/event-stream"
    )
