from pathlib import Path

from pydantic_settings import BaseSettings
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# env_file = os.path.join(BASE_DIR, ".env")
# print(env_file)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Law RAG Agent"
    # API_V1_STR: str = "/api/v1"

    OPENAI_API_BASE: str
    OPENAI_API_KEY: str

    # PostgreSQL 配置
    POSTGRESQL_DB: str
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int

    # Redis 配置
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int

    # 日志
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    class Config:
        # env_file = ".env"
        env_file = os.path.join(BASE_DIR, ".env")  # 从项目根目录加载.env文件，使用绝对路径

        case_sensitive = True  # 环境变量名称区分大小写
        env_file_encoding = "utf-8"  # 环境变量文件编码
        extra = "ignore"  # 忽略未定义的环境变量


settings = Settings()
