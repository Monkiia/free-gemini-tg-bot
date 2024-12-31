#!/bin/bash

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker 未运行，请先启动 Docker"
    exit 1
fi

# 检查是否提供了bot名称作为参数
if [ -z "$1" ]; then
    echo "请提供bot名称作为参数"
    echo "使用方式: ./start.sh <bot-name>"
    exit 1
fi

BOT_NAME=$1

# 确保配置目录存在
mkdir -p config/${BOT_NAME}

# 提示用户输入配置
echo "正在配置 Bot: ${BOT_NAME}"
echo "请输入配置信息："
read -p "Telegram Bot Token: " telegram_token
read -p "Gemini API Key: " gemini_key
read -p "Response Probability (0.0-1.0, 默认0.3): " probability

# 如果概率为空，使用默认值
probability=${probability:-0.3}

# 创建或更新.env文件
cat > config/${BOT_NAME}/.env << EOL
TELEGRAM_TOKEN=${telegram_token}
GEMINI_API_KEY=${gemini_key}
RESPONSE_PROBABILITY=${probability}
EOL

export BOT_NAME=${BOT_NAME}
export TELEGRAM_TOKEN=${telegram_token}
export GEMINI_API_KEY=${gemini_key}
export RESPONSE_PROBABILITY=${probability}

# 导出环境变量
export BOT_NAME

# 构建并启动容器
echo "正在启动 bot: ${BOT_NAME}..."

# 显示更多调试信息
echo "开始构建镜像..."
docker-compose build --no-cache

echo "启动容器..."
docker-compose up -d

# 检查容器状态
echo "检查容器状态..."
docker-compose ps

# 显示运行中的容器
echo "所有运行中的容器："
docker ps

echo "查看容器日志..."
docker-compose logs

echo "Bot ${BOT_NAME} 启动流程完成！"
echo "使用以下命令查看日志: docker-compose logs -f" 