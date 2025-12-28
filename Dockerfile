# ---------------------------------------
# 第一阶段：构建依赖导出层
# ---------------------------------------
# 修改点 1：使用 python:3.12-slim
FROM python:3.12-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY pyproject.toml poetry.lock* /tmp/

# 导出 requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# ---------------------------------------
# 第二阶段：构建最终运行镜像
# ---------------------------------------
# 修改点 2：使用 python:3.12-slim
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 可选：Python 3.12 有时对某些旧包的编译依赖要求较高
# 如果你在安装 psycopg2 (非 binary 版) 时报错，取消下面这行的注释
# RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# 安装依赖
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]