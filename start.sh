#!/bin/bash

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

# 导出环境变量
export BOT_NAME

# 构建并启动容器
echo "正在启动 bot: ${BOT_NAME}..."
docker-compose up --build -d

echo "Bot ${BOT_NAME} 已启动！"
echo "查看日志请使用: docker-compose logs -f" 