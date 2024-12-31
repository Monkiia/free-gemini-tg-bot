FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src ./src

# 创建配置文件目录
RUN mkdir -p /app/config

# 设置环境变量文件的默认位置
ENV ENV_FILE=/app/config/.env
ENV PYTHONPATH=/app

# 运行bot
CMD ["python", "-m", "src.bot.main"] 