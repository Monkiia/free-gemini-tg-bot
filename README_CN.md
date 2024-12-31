# Gemini 电报机器人

[English](README.md) | [中文](README_CN.md)

一个由 Google Gemini AI 驱动的 Telegram 群聊机器人。

## 功能特点

- 智能对话：使用 Google Gemini AI 生成回复
- 加密货币功能：
  - 实时价格查询
  - 技术指标分析（恐慌指数、彩虹图等）
  - 市场情绪分析
- 交互方式：
  - 通过 @ 直接与机器人对话
  - 根据设定概率随机回复群消息
- 上下文记忆：记住对话历史，实现连续对话
- 支持多实例：可同时运行多个机器人

## 使用案例

### 1. 加密货币查询
```
用户: @mybot btc价格
机器人: Bitcoin 当前价格: $65,432.21 USD

用户: @mybot 分析btc走势
机器人: 📊 BITCOIN 技术分析报告
😱 恐慌贪婪指数: 75 - 贪婪
🌈 彩虹图分析: 价格处于'合理'区域
📈 S2F模型分析: 当前价格处于模型预测范围的下方，可能被低估
📊 MVRV Z-Score: 2.1 - 市场估值适中，未到极端区域
⛏️ 矿工收入分析: 矿工收入稳定，哈希率处于历史高位

用户: @mybot eth价格如何
机器人: Ethereum 当前价格: $3,456.78 USD
```

### 2. 连续对话示例
```
用户: @mybot 比特币最近涨了吗
机器人: 让我查看一下...
[价格和分析信息]

用户: 你觉得现在适合买入吗
机器人: 根据之前的分析，目前市场情况是...
[基于上下文的分析建议]
```

## 开发中功能 (TBD)

1. 数据持久化
   - 保存历史数据
   - 用户偏好设置
   - 群组定制化配置

2. 定时任务
   - 每日市场总结
   - 重要指标提醒
   - 定期趋势分析

3. 数据可视化
   - 价格走势图表
   - 技术指标图形
   - 市场情绪仪表盘

4. LangChain 工具扩展
   - 自定义分析工具
   - 新闻聚合分析
   - 社交情绪分析

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

## 高级功能说明

### 上下文记忆
- 机器人能够记住对话历史
- 支持多轮对话推理
- 群组独立的对话记忆

### LangChain 工具系统
- 模块化工具设计
- 易于扩展新功能
- 支持自定义分析逻辑

## 注意事项

- 请妥善保管 API 密钥
- 每个机器人实例都会占用系统资源
- 定期检查日志确保运行正常
- 技术分析仅供参考，不构成投资建议