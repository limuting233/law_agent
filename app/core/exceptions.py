from core.status_code import AppStatus


class BusinessException(Exception):
    """
    业务异常类
    配合 AppStatus 枚举使用，用于在业务层中断逻辑并返回特定错误码
    """

    def __init__(self, status: AppStatus):
        """
        初始化业务异常实例
        :param status: 应用状态码枚举值
        """
        self.code = status.code
        self.error_message = status.error_message
        self.http_status = status.http_status

        # 调用父类构造函数，便于 Sentry 等日志工具捕获异常信息
        super().__init__(self.error_message)

    # def __str__(self):
    #     return f"[BusinessException] {self.code}: {self.error_message}"
