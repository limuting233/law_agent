from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from loguru import logger

from core.exceptions import BusinessException
from core.status_code import AppStatus


def global_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    """
    全局异常处理器，用于捕获所有未处理的异常（兜底）
    :param request: FastAPI 请求对象
    :param exception: 异常对象
    :return: JSONResponse 包含错误码、错误信息的 JSON 响应
    """
    logger.error(f"[GlobalException处理器] 未知异常: {str(exception)}")
    logger.exception(exception)  # 打印完整的堆栈信息
    return JSONResponse(
        status_code=AppStatus.server_error.http_status,
        content={
            "code": AppStatus.server_error.code,
            "message": "error",
            "error_message": AppStatus.server_error.error_message,
            "data": None,
        }
    )


def business_exception_handler(request: Request, exception: BusinessException) -> JSONResponse:
    """
    业务异常处理器函数
    :param request: FastAPI 请求对象
    :param exception: 业务异常对象
    :return: JSONResponse 包含错误码、错误信息的 JSON 响应
    """
    logger.error(f"[BusinessException处理器] 状态码: {exception.code}, 错误信息: {exception.error_message}")
    return JSONResponse(
        status_code=exception.http_status,
        content={
            "code": exception.code,
            "message": "error",
            "error_message": exception.error_message,
            "data": None,
        }
    )


def register_exception_handler(app: FastAPI) -> None:
    """
    将所有异常处理器注册到 FastAPI 实例上
    :param app: FastAPI 应用实例
    :return: None
    """
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
