import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from api.v1.router import api_router
from core.config import settings
from core.handlers import register_exception_handler
from core.logging import setup_logging

from loguru import logger
from db.redis import get_redis_client, RedisManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 启动时 ---
    await RedisManager.init()
    # register_exception_handler(app)
    # logger.info("全局异常处理器注册完成")
    yield
    # --- 关闭时 ---
    await RedisManager.close()
    # setup_logging()  # 初始化日志配置
    # logger.info("日志配置初始化完成")

    # yield


def create_app() -> FastAPI:
    """
    创建 FastAPI 应用实例

    :return: FastAPI 应用实例
    """
    app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

    # logger.info("正在初始化日志配置...")
    setup_logging()  # 初始化日志配置
    logger.info("日志配置初始化完成")

    register_exception_handler(app)
    # logger.info("全局异常处理器注册完成")



    logger.info("正在注册 API V1 路由...")
    app.include_router(api_router, prefix="/api/v1")
    logger.info("API V1 路由注册完成")

    return app


app = create_app()
