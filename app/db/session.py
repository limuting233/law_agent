from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
# from sqlalchemy.orm import sessionmaker

from core.config import settings

postgresql_url = f"postgresql+asyncpg://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOST}:{settings.POSTGRESQL_PORT}/{settings.POSTGRESQL_DB}"

async_postgresql_engine = create_async_engine(
    url=postgresql_url,
    pool_size=settings.POSTGRESQL_POOL_SIZE,
    max_overflow=settings.POSTGRESQL_MAX_OVERFLOW,
)

AsyncPostgresqlSessionLocal = async_sessionmaker(
    bind=async_postgresql_engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)
