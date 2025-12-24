from enum import Enum

from dataclasses import dataclass


@dataclass
class StatusDetail:
    """
    状态码详情数据类
    """
    code: int
    error_message: str
    http_status: int = 400  # 默认 HTTP 状态码


class AppStatus(Enum):
    """
    应用状态码枚举类
    """

    # --- 通用 ---
    # SUCCESS = StatusDetail(200, "Success", 200)
    server_error = StatusDetail(10000, "系统繁忙，请稍后重试", 500)
    params_error = StatusDetail(10001, "参数校验失败", 400)

    # --- 用户 ---
    auth_failed = StatusDetail(20001, "用户名或密码错误", 401)
    user_exists = StatusDetail(20002, "用户已存在", 400)
    token_expired = StatusDetail(20101, "登录已过期，请重新登录", 401)

    # --- 对话 ---
    quota_exceeded = StatusDetail(30003, "今日提问次数已达上限", 429)
    sensitive_content = StatusDetail(30005, "提问包含敏感内容", 400)
    agent_error = StatusDetail(30006, "智能体服务异常", 502)

    # --- 知识库 ---
    file_format_error = StatusDetail(40001, "不支持的文件格式", 415)
    file_parse_error = StatusDetail(40003, "文件解析失败", 500)

    @property
    def code(self):
        """
        获取状态码值
        :return: 状态码值
        """
        return self.value.code

    @property
    def error_message(self):
        """
        获取错误信息
        :return: 错误信息
        """
        return self.value.error_message

    @property
    def http_status(self):
        """
        获取 HTTP 状态码
        :return: HTTP 状态码
        """
        return self.value.http_status
