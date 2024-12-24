# Free Gemini Telegram Bot

[English](README.md) | [中文](README_CN.md)

A Telegram group chat bot powered by Google Gemini AI. It can:
- Randomly reply to group messages (configurable probability)
- Always respond when mentioned (@)
- Generate intelligent responses using AI
- Support running multiple bot instances

## Prerequisites

### 1. Install Docker
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Open Docker Desktop application after installation

### 2. Get Telegram Bot Token
1. Find [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Follow instructions to set up your bot
4. Save the Bot Token

### 3. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Login with Google account
3. Click "Create API Key"
4. Save the API Key

## Quick Start

1. Download project files
2. Open terminal, navigate to project directory
3. Add execution permissions:
```bash
chmod +x start.sh manage.sh
```

4. Start the bot:
```bash
./start.sh mybot
```

5. Enter when prompted:
   - Telegram Bot Token (from @BotFather)
   - Gemini API Key (from Google AI Studio)
   - Response Probability (0.0-1.0, default 0.3)

6. Add the bot to your Telegram group

## Management Commands

Use `manage.sh` to manage your bot:
```bash
./manage.sh <bot_name> <command>
```

Available commands:
- `logs`: View running logs
- `stop`: Stop the bot
- `start`: Start the bot
- `restart`: Restart the bot

Examples:
```bash
# View logs
./manage.sh mybot logs

# Stop bot
./manage.sh mybot stop
```

## Running Multiple Bots

You can run multiple bot instances simultaneously:
```bash
# Start first bot
./start.sh bot1

# Start second bot
./start.sh bot2
```

Note: Each bot needs its own Telegram Bot Token

## Usage Guide

1. Random Replies
   - Bot replies to group messages based on set probability
   - Probability of 0.3 means about 30% of messages get replies

2. @ Mentions
   - Bot always responds when mentioned at start of message
   - Example: `@mybot hello`

3. Customize Bot Personality
   - Modify `src/bot/prompts.py` to customize bot's reply style
   - Edit `CHAT_PROMPT` variable to change bot's personality and response style
   - Examples of possible personalities:
     - Professional technical advisor
     - Humorous entertainer
     - Domain-specific expert
     - Specific role-play character

## Common Issues

1. Docker Not Running
   - Error: `Docker daemon is not running`
   - Solution: Open Docker Desktop application

2. Bot Not Responding
   - Check logs: `./manage.sh <bot_name> logs`
   - Verify Bot Token is correct
   - Confirm bot is added to group

3. Need to Modify Configuration
   - Stop bot: `./manage.sh <bot_name> stop`
   - Restart: `./start.sh <bot_name>`

## Notes

- Keep API keys secure
- Each bot instance uses system resources
- Regularly check logs for normal operation