#!/bin/bash

# 检查参数
if [ $# -lt 2 ]; then
    echo "使用方式: ./manage.sh <bot-name> <command>"
    echo "可用命令: logs, stop, start, restart, follow-logs"
    exit 1
fi

BOT_NAME=$1
COMMAND=$2

export BOT_NAME

case $COMMAND in
    "logs")
        docker-compose logs
        ;;
    "follow-logs")
        docker-compose logs -f
        ;;
    "stop")
        docker-compose down
        ;;
    "start")
        docker-compose up -d
        ;;
    "restart")
        docker-compose restart
        ;;
    *)
        echo "未知命令: $COMMAND"
        echo "可用命令: logs, stop, start, restart, follow-logs"
        exit 1
        ;;
esac 