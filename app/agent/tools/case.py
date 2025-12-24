from langchain_core.tools import tool


@tool
def search_case(query: str) -> str:
    """
    搜索法律案例
    :param query: 搜索查询
    :return: 法律案例列表
    """
    return f"根据{query}搜索到的法律案例列表，案例1，案例2，案例3"
