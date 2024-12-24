import random
import traceback
import asyncio
import google.generativeai as genai
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from telegram import Update
from telegram.error import TimedOut, NetworkError
from .config import Config
from .prompts import CHAT_PROMPT

class ChatBot:
    def __init__(self):
        print(f"Initializing bot with token: {Config.TELEGRAM_TOKEN[:10]}...")
        # 设置更长的超时时间
        self.application = (
            Application.builder()
            .token(Config.TELEGRAM_TOKEN)
            .connect_timeout(30.0)
            .read_timeout(30.0)
            .write_timeout(30.0)
            .build()
        )
        
        # 初始化 Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # 注册消息处理器
        print("Registering handlers...")
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
        
        # 添加错误处理器
        self.application.add_error_handler(self.error_handler)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """处理错误"""
        print(f"Exception while handling an update:")
        traceback.print_exception(context.error)

    async def send_message_with_retry(self, message, reply_text, max_retries=3):
        """带重试的消息发送"""
        for attempt in range(max_retries):
            try:
                await message.reply_text(reply_text)
                return True
            except (TimedOut, NetworkError) as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    print(f"Failed to send message after {max_retries} attempts: {e}")
                    return False
                print(f"Attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(1)  # 等待1秒后重试
        return False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理 /start 命令"""
        try:
            print(f"Received /start command from {update.effective_user.id}")
            response_text = "Bot is active! Send me some messages and I'll respond."
            print(f"Sending response: {response_text}")
            success = await self.send_message_with_retry(update.message, response_text)
            if success:
                print("Response sent successfully")
            else:
                print("Failed to send response")
        except Exception as e:
            print(f"Error in start_command: {e}")
            traceback.print_exc()

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """处理收到的消息"""
        try:
            # 打印详细的消息信息
            print(f"\nReceived message:")
            print(f"From user ID: {update.effective_user.id}")
            print(f"Username: {update.effective_user.username}")
            print(f"Chat type: {update.effective_chat.type}")
            print(f"Chat ID: {update.effective_chat.id}")
            print(f"Text: {update.message.text}")
            
            message_text = update.message.text
            
            # 检查是否是 @ 开头的消息
            is_mentioned = message_text.startswith('@')
            
            # 如果不是 @ 开头，则进行概率检查
            if not is_mentioned and random.random() > Config.RESPONSE_PROBABILITY:
                print("Skipping message due to probability check")
                return
                
            print("Generating AI response...")
            # 调用 Gemini API
            # 如果是 @ 开头，移除 @ 及其后面的用户名部分
            if is_mentioned:
                # 找到第一个空格，截取后面的实际消息内容
                _, _, actual_message = message_text.partition(' ')
                if not actual_message.strip():  # 如果消息为空
                    print("Empty message after mention, skipping...")
                    return
                message_text = actual_message
            
            # 使用格式化的prompt
            prompt = CHAT_PROMPT.format(message=message_text)
            response = self.model.generate_content(prompt)
            
            # 发送回复
            reply_text = response.text
            print(f"Sending AI response: {reply_text}")
            success = await self.send_message_with_retry(update.message, reply_text)
            if success:
                print("Response sent successfully")
            else:
                print("Failed to send response")
            
        except Exception as e:
            print(f"Error in handle_message: {e}")
            traceback.print_exc()

    def run(self):
        """运行bot"""
        print("Starting bot...")
        self.application.run_polling(
            drop_pending_updates=True,
            pool_timeout=30.0,
            read_timeout=30.0,
            write_timeout=30.0,
            connect_timeout=30.0
        )