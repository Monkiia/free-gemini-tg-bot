# Gemini 电报机器人

一个由 Google Gemini AI 驱动的 Telegram 群聊机器人。

## 功能特点

- 智能对话：使用 Google Gemini AI 生成回复
- 加密货币功能：
  - 实时价格查询
  - 技术指标分析
  - 市场情绪分析
- 交互方式：
  - 通过 @ 直接与机器人对话
  - 根据设定概率随机回复群消息
- 支持多实例：可同时运行多个机器人

## 使用前提

### 1. 安装 Docker
- 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- 安装后启动 Docker Desktop 应用

### 2. 获取 Telegram Bot Token
1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 命令
3. 按照提示设置机器人
4. 保存获得的 Bot Token

### 3. 获取 Gemini API Key
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用 Google 账号登录
3. 点击 "Create API Key"
4. 保存获得的 API Key

## 快速开始

1. 下载项目文件
2. 打开终端，进入项目目录
3. 添加执行权限：
```bash
chmod +x start.sh manage.sh
```

4. 启动机器人：
```bash
./start.sh mybot
```

5. 根据提示输入：
   - Telegram Bot Token（从 @BotFather 获取）
   - Gemini API Key（从 Google AI Studio 获取）
   - 回复概率（0.0-1.0，默认 0.3）

6. 将机器人添加到 Telegram 群组

## 管理命令

使用 `manage.sh` 管理机器人：
```bash
./manage.sh <bot名称> <命令>
```

可用命令：
- `logs`: 查看运行日志
- `stop`: 停止机器人
- `start`: 启动机器人
- `restart`: 重启机器人

示例：
```bash
# 查看日志
./manage.sh mybot logs

# 停止机器人
./manage.sh mybot stop
```

## 运行多个实例

可以同时运行多个机器人实例：
```bash
# 启动第一个机器人
./start.sh bot1

# 启动第二个机器人
./start.sh bot2
```

注意：每个机器人需要独立的 Telegram Bot Token

## 使用说明

1. 直接对话
   - 在群组中 @ 机器人即可对话
   - 例如：`@mybot 你好`

2. 加密货币功能
   - 查询价格：`@mybot btc价格`
   - 技术分析：`@mybot 分析btc走势`
   - 市场情绪：`@mybot btc市场分析`

3. 随机回复
   - 机器人会根据设定的概率随机回复群消息
   - 概率为 0.3 表示大约 30% 的消息会被回复

## 常见问题

1. Docker 未运行
   - 错误：`Docker daemon is not running`
   - 解决：启动 Docker Desktop 应用

2. 机器人无响应
   - 检查日志：`./manage.sh <bot名称> logs`
   - 验证 Bot Token 是否正确
   - 确认机器人已被添加到群组

3. 需要修改配置
   - 停止机器人：`./manage.sh <bot名称> stop`
   - 重新启动：`./start.sh <bot名称>`

## 注意事项

- 请妥善保管 API 密钥
- 每个机器人实例都会占用系统资源
- 定期检查日志确保运行正常