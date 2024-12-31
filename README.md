# Free Gemini Telegram Bot

[English](README.md) | [中文](README_CN.md)

A Telegram group chat bot powered by Google Gemini AI, specialized in cryptocurrency analysis.

## Features

- AI-Powered Chat:
  - Powered by Google Gemini AI
  - Context-aware conversations
  - Group-specific memory
- Cryptocurrency Tools:
  - Real-time price queries
  - Technical indicators (Fear & Greed Index, Rainbow Chart, etc.)
  - Market sentiment analysis
- Interaction Modes:
  - Direct @ mentions
  - Random response with configurable probability
- Multi-Instance Support:
  - Run multiple bots simultaneously
  - Independent configurations

## Usage Examples

### 1. Cryptocurrency Queries
```
User: @mybot btc price
Bot: Bitcoin Current Price: $65,432.21 USD

User: @mybot analyze btc trend
Bot: 📊 BITCOIN Technical Analysis Report
😱 Fear & Greed Index: 75 - Greedy
🌈 Rainbow Chart: Price in 'Fair Value' zone
📈 S2F Model: Price below model prediction, possibly undervalued
📊 MVRV Z-Score: 2.1 - Market valuation moderate
⛏️ Mining Analysis: Stable miner revenue, hashrate at ATH

User: @mybot eth price
Bot: Ethereum Current Price: $3,456.78 USD
```

### 2. Contextual Conversation
```
User: @mybot has bitcoin been rising lately?
Bot: Let me check...
[Price and analysis information]

User: do you think it's a good time to buy?
Bot: Based on the previous analysis, the current market conditions...
[Context-aware analysis and suggestion]
```

## Upcoming Features (TBD)

1. Data Persistence
   - Historical data storage
   - User preferences
   - Group customization

2. Scheduled Tasks
   - Daily market summaries
   - Important indicator alerts
   - Regular trend analysis

3. Data Visualization
   - Price trend charts
   - Technical indicator graphs
   - Market sentiment dashboard

4. LangChain Tool Extensions
   - Custom analysis tools
   - News aggregation
   - Social sentiment analysis

## Prerequisites

### 1. Install Docker
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Launch Docker Desktop after installation

### 2. Get Telegram Bot Token
1. Find [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow the setup instructions
4. Save the Bot Token

### 3. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Save the API Key

## Quick Start

1. Download project files
2. Open terminal in project directory
3. Add execution permissions:
```bash
chmod +x start.sh manage.sh
```

4. Start bot:
```bash
./start.sh mybot
```

5. Enter when prompted:
   - Telegram Bot Token (from @BotFather)
   - Gemini API Key (from Google AI Studio)
   - Response Probability (0.0-1.0, default 0.3)

6. Add bot to Telegram group

## Management Commands

Use `manage.sh` to control the bot:
```bash
./manage.sh <bot-name> <command>
```

Available commands:
- `logs`: View historical logs
- `follow-logs`: Real-time log tracking
- `stop`: Stop bot
- `start`: Start bot
- `restart`: Restart bot

Example:
```bash
# View historical logs
./manage.sh mybot logs

# Real-time log tracking
./manage.sh mybot follow-logs

# Stop bot
./manage.sh mybot stop
```

## Logging System

### 1. Log Locations
- Console output: Real-time status
- File logs: `logs/<bot-name>/bot.log`

### 2. Log Contents
- Startup information
- Conversation records
- Tool invocations
- Error messages
- AI thinking process

### 3. Log Configuration
- Auto-rotation: New file created after 10MB
- History retention: Keeps up to 5 historical files
- Format: timestamp - module - level - message

### 4. Viewing Logs
```bash
# View historical logs
cat logs/mybot/bot.log

# Real-time tracking
tail -f logs/mybot/bot.log

# Using manage.sh
./manage.sh mybot follow-logs
```

## Running Multiple Instances

You can run multiple bot instances:
```bash
# Start first bot
./start.sh bot1

# Start second bot
./start.sh bot2
```

Note: Each bot needs its own Telegram Bot Token

## Usage Guide

1. Direct Interaction
   - @ mention the bot in group
   - Example: `@mybot hello`

2. Crypto Features
   - Price check: `@mybot btc price`
   - Technical analysis: `@mybot analyze btc trend`
   - Market sentiment: `@mybot btc market analysis`

3. Random Responses
   - Bot responds randomly based on set probability
   - 0.3 probability means ~30% messages get responses

## Advanced Features

### Context Memory
- Remembers conversation history
- Supports multi-turn reasoning
- Group-specific memory isolation

### LangChain Tool System
- Modular tool design
- Easy to extend
- Custom analysis support

## Troubleshooting

1. Docker Not Running
   - Error: `Docker daemon is not running`
   - Solution: Start Docker Desktop

2. Bot Not Responding
   - Check logs: `./manage.sh <bot_name> logs`
   - Verify Bot Token
   - Confirm bot is in group

3. Configuration Changes
   - Stop bot: `./manage.sh <bot_name> stop`
   - Restart: `./start.sh <bot_name>`

## Notes

- Keep API keys secure
- Each instance uses system resources
- Check logs regularly
- Technical analysis is for reference only