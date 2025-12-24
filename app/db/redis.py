from loguru import logger
# from redis import from_url
from redis.asyncio import Redis,from_url

from core.config import settings

redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"


class RedisManager:
    """
    Redis 单例管理器
    """

    _client: Redis | None = None

    @classmethod
    async def init(cls):
        """
        初始化 Redis 连接池
        :return:
        """
        if cls._client is None:
            logger.info(f"正在创建Redis连接池...")

            cls._client = from_url(
                url=redis_url,
                encoding="utf-8",
                decode_responses=True,  # 自动解码为字符串
                socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
                socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
                max_connections=settings.REDIS_POOL_MAX_CONNECTIONS,
                health_check_interval=settings.REDIS_POOL_HEALTH_CHECK,

            )
            # 测试连接
            await cls._client.ping()
            logger.info(f"Redis连接池创建成功")

    @classmethod
    async def close(cls):
        """
        关闭 Redis 连接池
        :return:
        """
        if cls._client is not None:
            logger.info(f"正在关闭Redis连接池...")
            await cls._client.close()
            cls._client = None
            logger.info(f"Redis连接池已关闭")

    @classmethod
    def get_client(cls) -> Redis:
        """
        获取 Redis 客户端
        :return: Redis 客户端
        """
        if cls._client:
            return cls._client
        else:
            raise RuntimeError("Redis 连接池未初始化")


# 导出获取客户端的方法，方便调用
def get_redis_client() -> Redis:
    return RedisManager.get_client()
