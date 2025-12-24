import asyncio
import time

from langchain_core.messages import AIMessageChunk, ToolMessage

from agent.executor import law_agent
from core.status_code import AppStatus
from schemas.request.chat import ChatRequest, Message
from loguru import logger

from schemas.response.stream import StreamResponse, TextChunkMeta, ErrorMeta, ToolUseMeta, WorkflowStartMeta, DoneMeta


class ChatService:
    """
    聊天服务类，用于处理用户聊天相关操作
    """

    async def chat_stream(self, request: ChatRequest):
        chat_id = request.chat_id  # 获取聊天会话ID
        message = request.message  # 获取用户消息

        content = message.content.strip()  # 提取文本消息并去除首尾空格

        try:

            yield StreamResponse(
                event="workflow_start",
                data=None,
                meta=WorkflowStartMeta(
                    chat_id=chat_id,
                    timestamp=int(time.time() * 1000),
                )
            )

            # 初始化计数器，用于前端流式排序
            chunk_index = 0

            # 调用agent生成回复
            async for mode, chunk in law_agent.astream(
                    input={"messages": [{"role": "user", "content": content}]},
                    stream_mode=["messages", "updates"]
            ):
                # mode,chunk 示例:
                # ('messages', (AIMessageChunk(content='你好', additional_kwargs={}, response_metadata={'model_provider': 'openai'}, id='lc_run--019b4ec7-f94f-7af2-896d-a4e288eecee1'), {'langgraph_step': 1, 'langgraph_node': 'model', 'langgraph_triggers': ('branch:to:model',), 'langgraph_path': ('__pregel_pull', 'model'), 'langgraph_checkpoint_ns': 'model:5610268a-3758-f49d-4cbd-442e465add7d', 'checkpoint_ns': 'model:5610268a-3758-f49d-4cbd-442e465add7d', 'ls_provider': 'openai', 'ls_model_name': 'gpt-4.1-mini', 'ls_model_type': 'chat', 'ls_temperature': None}))
                # ...
                # ('updates', {'model': {'messages': [AIMessage(content='你好！有什么我可以帮你的吗？', additional_kwargs={}, response_metadata={'finish_reason': 'stop', 'model_name': 'gpt-4.1-mini-2025-04-14', 'system_fingerprint': 'fp_3dcd5944f5', 'model_provider': 'openai'}, id='lc_run--019b4ec7-f94f-7af2-896d-a4e288eecee1', usage_metadata={'input_tokens': 8, 'output_tokens': 10, 'total_tokens': 18, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}})
                
                # print(mode)
                # print(chunk)

                if mode == "messages":
                    msg_chunk, meta_info = chunk  # 解包消息块和元信息
                    if isinstance(msg_chunk, AIMessageChunk) and msg_chunk.content:
                        chunk_index += 1
                        yield StreamResponse(
                            event="text_chunk",
                            data=msg_chunk.content,
                            meta=TextChunkMeta(
                                chat_id=chat_id,
                                timestamp=int(time.time() * 1000),
                                # trace_id=msg_chunk.id,
                                index=chunk_index,
                                # node=meta_info["langgraph_node"],
                                # model=meta_info["ls_model_name"],

                            )
                        )
                    elif isinstance(msg_chunk, ToolMessage) and msg_chunk.content:
                        yield StreamResponse(
                            event="tool_use",
                            data=msg_chunk.content,
                            meta=ToolUseMeta(
                                chat_id=chat_id,
                                timestamp=int(time.time() * 1000),
                                tool_name=msg_chunk.name
                            )
                        )

                elif mode == "updates":
                    pass

            yield StreamResponse(
                event="done",
                data=None,
                meta=DoneMeta(
                    chat_id=chat_id,
                    timestamp=int(time.time() * 1000),
                )
            )




        except Exception as e:
            logger.error(f"law_agent流式调用异常: {str(e)}")
            yield StreamResponse(
                event="error",
                data=None,
                meta=ErrorMeta(
                    chat_id=chat_id,
                    trace_id=None,
                    timestamp=int(time.time() * 1000),
                    code=AppStatus.agent_error.code,
                    error_message=AppStatus.agent_error.error_message,
                )
            )

#
# if __name__ == '__main__':
#     chat = ChatService()
#     asyncio.run(chat.chat_stream(ChatRequest(chat_id="123", message=Message(content="查询离婚的法律案例"))))
