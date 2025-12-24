from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db.session import AsyncPostgresqlSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取异步数据库会话
    :return: 异步数据库会话
    """
    async with AsyncPostgresqlSessionLocal() as session:
        yield session
        # try:
        #     yield session
        # finally:
        #     await session.close()
