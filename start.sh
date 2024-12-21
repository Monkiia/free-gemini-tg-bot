#!/bin/bash

# 提示用户输入bot名称
read -p "Bot Name (用于区分不同的bot实例): " bot_name

# 确保配置目录存在
mkdir -p config/${bot_name}

# 提示用户输入配置
echo "请输入配置信息："
read -p "Telegram Bot Token: " telegram_token
read -p "Gemini API Key: " gemini_key
read -p "Response Probability (0.0-1.0, 默认0.3): " probability

# 如果概率为空，使用默认值
probability=${probability:-0.3}

# 创建或更新.env文件
cat > config/${bot_name}/.env << EOL
TELEGRAM_TOKEN=${telegram_token}
GEMINI_API_KEY=${gemini_key}
RESPONSE_PROBABILITY=${probability}
EOL

# 设置环境变量
export BOT_NAME=${bot_name}

# 构建并启动容器
echo "正在启动bot..."
docker-compose up --build -d

echo "Bot已启动！"
echo "查看日志请使用: docker-compose logs -f" 