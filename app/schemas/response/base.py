from typing import TypeVar, Generic, Literal, Optional

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """
    接口基础响应模型
    """
    code: int = Field(default=200, description="业务状态码")
    message: Literal["success", "error"] = Field(default="success", description="请求是否成功")
    error_message: Optional[str] = Field(default=None, description="错误信息")
    data: T = Field(default=None, description="响应数据")


def success(data: Optional[T] = None) -> BaseResponse[T]:
    """
    成功响应
    :param data: 响应数据
    :return: 成功响应模型
    """
    return BaseResponse(code=200, message="success", data=data)


def error(code: int, error_message: str) -> BaseResponse[T]:
    """
    错误响应
    :param code: 错误码
    :param error_message: 错误信息
    :return: 错误响应模型
    """
    return BaseResponse(code=code, message="error", error_message=error_message)
