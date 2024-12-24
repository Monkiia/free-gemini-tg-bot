# Telegram AI 群聊机器人

[English](README.md) | [中文](README_CN.md) 

echo '# Telegram AI 群聊机器人

一个基于 Google Gemini AI 的 Telegram 群聊机器人。它可以：
- 随机回复群消息（可设置概率）
- 被 @ 时必定回复
- 使用 AI 生成智能回复
- 支持运行多个机器人实例

## 准备工作

### 1. 安装 Docker
- 下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- 安装后打开 Docker Desktop 应用

### 2. 获取 Telegram Bot Token
1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 命令
3. 按提示设置机器人名称
4. 保存获得的 Bot Token

### 3. 获取 Gemini API Key
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录 Google 账号
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

5. 按提示输入：
   - Telegram Bot Token（从 @BotFather 获取）
   - Gemini API Key（从 Google AI Studio 获取）
   - Response Probability（回复概率，0.0-1.0，默认 0.3）

6. 将机器人添加到 Telegram 群组

## 管理命令

使用 `manage.sh` 管理机器人：
```bash
./manage.sh <机器人名称> <命令>
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

## 运行多个机器人

可以同时运行多个机器人实例：
```bash
# 启动第一个机器人
./start.sh bot1

# 启动第二个机器人
./start.sh bot2
```

注意：每个机器人需要独立的 Telegram Bot Token

## 使用说明

1. 随机回复
   - 机器人会根据设定的概率随机回复群消息
   - 概率为 0.3 表示约 30% 的消息会被回复

2. @ 回复
   - 在消息开头 @ 机器人时，必定会收到回复
   - 例如：`@mybot 你好`

3. 自定义机器人个性
   - 可以通过修改 `src/bot/prompts.py` 文件来自定义机器人的回复风格
   - 编辑 `CHAT_PROMPT` 变量来改变机器人的性格特征和回复方式
   - 例如，可以将机器人设定为：
     - 专业的技术顾问
     - 幽默风趣的段子手
     - 特定领域的专家
     - 特定角色扮演

## 常见问题

1. Docker 未运行
   - 错误信息：`Docker daemon is not running`
   - 解决：打开 Docker Desktop 应用

2. 机器人不响应
   - 检查日志：`./manage.sh <机器人名称> logs`
   - 确认 Bot Token 正确
   - 确认已将机器人添加到群组

3. 需要修改配置
   - 停止机器人：`./manage.sh <机器人名称> stop`
   - 重新运行：`./start.sh <机器人名称>`

## 注意事项

- 请妥善保管 API 密钥
- 每个机器人实例会占用一定系统资源
- 建议定期查看日志确保正常运行' > README.md