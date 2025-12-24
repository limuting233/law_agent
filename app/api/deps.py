from typing import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from db.redis import get_redis_client
from db.session import AsyncPostgresqlSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency: 获取异步数据库会话
    :return: 异步数据库会话
    """
    async with AsyncPostgresqlSessionLocal() as session:
        yield session
        # try:
        #     yield session
        # finally:
        #     await session.close()


def get_redis() -> Redis:
    """
    Dependency: 获取异步 Redis 客户端
    :return: Redis
    """
    return get_redis_client()
