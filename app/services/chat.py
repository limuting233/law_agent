import asyncio
import json
import time
import uuid

from langchain_core.messages import AIMessageChunk, ToolMessage, SystemMessage, HumanMessage, AIMessage
from redis.asyncio import Redis
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from agent import executor
from core.status_code import AppStatus
from models.chat import ChatSession, ChatMessage
from schemas.request.chat import ChatRequest, Message
from loguru import logger

from schemas.response.stream import StreamResponse, StartEvent, MessageEvent


class ChatService:
    """
    聊天服务类，用于处理用户聊天相关操作
    """

    async def chat_stream(self, request: ChatRequest, db: AsyncSession, redis_client: Redis):
        session_id = request.session_id  # 获取聊天会话ID

        message = request.message  # 获取用户消息

        content = message.content.strip()  # 提取文本消息并去除首尾空格

        try:
            try:
                if not session_id:
                    # 没有会话ID，需要创建一个新的会话ID，代表这是用户首次开启这个会话
                    new_session_id = str(uuid.uuid4())
                    # 在postgres数据库中创建一个新的会话记录
                    new_session = ChatSession(
                        id=new_session_id,
                        user_id="user_1",
                        title=content[0:10] if len(content) > 10 else content,
                        is_deleted=False,
                        created_at=int(time.time() * 1000),
                        updated_at=int(time.time() * 1000),
                    )
                    db.add(new_session)
                    await db.commit()
                    # session_id = new_session_id
            except Exception as e:
                raise Exception(f"创建新会话失败,{str(e)}")

            try:
                history_messages = []
                if session_id:
                    # 从redis中查询历史聊天记录
                    history = await redis_client.lrange(f"chat_history:{session_id}", 0, -1)
                    logger.info(f"从redis中查询会话{session_id}的历史聊天记录，共{len(history)}条")
                    if history:
                        # redis中存在历史记录

                        # 解析历史聊天记录
                        for msg in history:
                            msg = json.loads(msg)
                            if msg["type"] == "system":
                                history_messages.append(SystemMessage(**msg))
                            elif msg["type"] == "human":
                                history_messages.append(HumanMessage(**msg))
                            elif msg["type"] == "ai":
                                history_messages.append(AIMessage(**msg))
                    else:
                        # 无历史记录时，需要去postgres数据库里查询该会话的所有聊天记录，
                        # result = await db.execute(
                        #     select(func.count(ChatMessage.id)).where(ChatMessage.session_id == session_id))
                        # message_count = result.scalar()
                        # logger.info(f"从postgres数据库中查询会话{session_id}的聊天记录，共{message_count}条")
                        # 用户时隔很久没有与智能体交互，现在又开始与智能体交互，需要重新初始化历史记录
                        # 查询postgres数据库中该会话的所有聊天记录
                        result = await db.execute(select(ChatMessage).where(ChatMessage.session_id == session_id))
                        db_messages = result.scalars().all()
                        # 拿到所有的聊天记录，然后把他们放在redis中
                        redis_messages = []
                        for msg in db_messages:
                            redis_messages.append(json.dumps(msg.raw_data, ensure_ascii=False))
                            if msg.type == "system":
                                history_messages.append(SystemMessage(**msg.raw_data))
                            elif msg.type == "human":
                                history_messages.append(HumanMessage(**msg.raw_data))
                            elif msg.type == "ai":
                                history_messages.append(AIMessage(**msg.raw_data))
                        # 把所有的聊天记录写入redis
                        # await redis_client.rpush(f"chat_history:{session_id}", *redis_messages)
                        async with redis_client.pipeline() as pipe:
                            pipe.rpush(f"chat_history:{session_id}", *redis_messages)  # 把所有的聊天记录写入redis
                            pipe.expire(f"chat_history:{session_id}", 24 * 60 * 60)  # 设置过期时间为24小时
                            await pipe.execute()


            except Exception as e:
                raise Exception(f"查询会话{session_id}的历史聊天记录失败，{str(e)}")

            try:
                if not session_id:
                    session_id = new_session_id
                yield StreamResponse(
                    event="start",
                    data=StartEvent(
                        session_id=session_id,
                        start_at=int(time.time() * 1000),
                    )
                )

                # # 初始化计数器，用于前端流式排序
                # chunk_index = 0

                config = {"configurable": {"thread_id": session_id}}

                async for mode, chunk in executor.law_agent.astream(
                        input={
                            "messages": [HumanMessage(content=content)],
                            "user_id": "user_1",
                        },
                        stream_mode=["messages", "updates"],
                        config=config,
                ):
                    # logger.debug(f"mode: {mode}, chunk: {chunk}")
                    if mode == "messages":
                        # 处理messages模式下的chunk
                        msg_chunk, meta_info = chunk
                        if isinstance(msg_chunk, AIMessageChunk) and msg_chunk.content:
                            # chunk_index += 1
                            yield StreamResponse(
                                event="message",
                                data=MessageEvent(
                                    content=msg_chunk.content
                                )
                            )
                            # pass

                    elif mode == "updates":
                        # 处理updates模式下的chunk

                        pass

                state = await executor.law_agent.aget_state(config)
                print(state.values["messages"])
            except Exception as e:
                # logger.exception(f"law_agent流式调用异常, {str(e)}")
                raise Exception(f"law_agent流式调用异常, {str(e)}")


        except Exception as e:
            logger.error(f"LawAgent运行异常: {str(e)}")

#
# if __name__ == '__main__':
#     chat = ChatService()
#     asyncio.run(chat.chat_stream(ChatRequest(chat_id="123", message=Message(content="查询离婚的法律案例"))))
