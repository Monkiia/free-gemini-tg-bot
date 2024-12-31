import os
import logging
from telegram import Update, MessageEntity, Chat
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram.constants import ChatAction
import random
from ..chains.chat import ChatChain
from ..memory.memory import GroupMemory
from ..bot.config import Config

logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(self):
        """初始化机器人"""
        # 使用 Config 类获取配置
        self.token = Config.TELEGRAM_TOKEN
        self.response_probability = float(Config.RESPONSE_PROBABILITY)
        
        if not self.token:
            raise ValueError("Telegram bot token not found in environment variables")
        
        # 创建应用
        self.application = Application.builder().token(self.token).build()
        
        # 群组记忆
        self.group_memories = {}
        
        # 注册处理器
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("Bot initialized with token: %s...", self.token[:8])

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /start 命令"""
        await update.message.reply_text("你好！我是一个由 Gemini AI 驱动的加密货币助手。")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理群组消息"""
        try:
            message = update.message
            chat_id = message.chat_id
            
            # 检查是否是群组消息
            if not message.chat.type in ["group", "supergroup"]:
                return
            
            # 获取或创建群组记忆
            if chat_id not in self.group_memories:
                self.group_memories[chat_id] = GroupMemory(chat_id)
            
            memory = self.group_memories[chat_id]
            chain = ChatChain(memory=memory)
            
            # 检查是否@机器人或随机回复
            bot_mentioned = False
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntity.MENTION:
                        mention = message.text[entity.offset:entity.offset + entity.length]
                        if mention.replace("@", "") == context.bot.username:
                            bot_mentioned = True
                            break
            
            should_respond = bot_mentioned or (
                random.random() < self.response_probability
            )
            
            if should_respond:
                logger.info(f"Processing message in group {chat_id}")
                # 发送"正在输入"状态
                await context.bot.send_chat_action(
                    chat_id=chat_id,
                    action=ChatAction.TYPING
                )
                
                # 处理消息
                response = await chain.run(message.text)
                await message.reply_text(response)
                logger.info(f"Responded in group {chat_id}")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            await message.reply_text("抱歉，处理消息时出现错误。")

    def run(self):
        """运行机器人"""
        logger.info("Starting bot...")
        self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
