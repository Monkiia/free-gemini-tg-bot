from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from ..chains import ChatChain
from ..memory import GroupMemory
from ..tools import CryptoPriceTool
from .config import Config
import asyncio
import random

class ChatBot:
    def __init__(self):
        self.application = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        self.memories = {}  # 群组记忆
        self.tools = {
            "crypto_price": CryptoPriceTool()
        }
        self._running = False
        self.response_probability = Config.RESPONSE_PROBABILITY
        
        self._setup_handlers()

    def _setup_handlers(self):
        # 处理所有文本消息
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.handle_message
            )
        )

    def _get_or_create_memory(self, group_id: int) -> GroupMemory:
        if group_id not in self.memories:
            self.memories[group_id] = GroupMemory(group_id)
        return self.memories[group_id]

    def _should_respond(self, update: Update) -> bool:
        """判断是否应该回应消息"""
        # 获取消息文本和 bot 信息
        message = update.message
        bot_user = self.application.bot.username

        # 如果被@，一定回应
        if message.text.startswith(f"@{bot_user}"):
            return True
            
        # 如果是私聊，一定回应
        if message.chat.type == "private":
            return True
            
        # 根据概率决定是否回应
        return random.random() < self.response_probability

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理消息"""
        # 判断是否需要回应
        if not self._should_respond(update):
            return

        try:
            # 获取群组记忆
            group_id = update.effective_chat.id
            memory = self._get_or_create_memory(group_id)
            
            # 处理消息文本
            message_text = update.message.text
            bot_user = self.application.bot.username
            
            # 如果是@消息，移除@部分
            if message_text.startswith(f"@{bot_user}"):
                message_text = message_text[len(f"@{bot_user}"):].strip()
            
            # 如果消息为空，不处理
            if not message_text:
                return
            
            # 生成回复
            chain = ChatChain(memory=memory)
            response = await chain.run(message_text)
            
            # 发送回复
            await update.message.reply_text(response)
            
        except Exception as e:
            print(f"Error handling message: {e}")
            await update.message.reply_text("抱歉，处理消息时出现错误。")

    async def start(self):
        """启动bot"""
        if self._running:
            return

        try:
            print("Initializing bot...")
            await self.application.initialize()
            await self.application.start()
            
            print("Bot is running...")
            self._running = True
            
            # 启动轮询（异步方式）
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
                
        except Exception as e:
            print(f"Error during start: {e}")
            await self.stop()
            raise

    async def stop(self):
        """停止bot"""
        if not self._running:
            return

        try:
            print("Stopping bot...")
            self._running = False
            
            # 停止应用
            try:
                if self.application.updater and self.application.updater.running:
                    await self.application.updater.stop()
                if self.application.running:
                    await self.application.stop()
                await self.application.shutdown()
            except Exception as e:
                print(f"Error shutting down application: {e}")
            
            print("Bot stopped")
        except Exception as e:
            print(f"Error during shutdown: {e}")
            raise

    @property
    def running(self):
        return self._running
