import os
from .bot import ChatBot
from ..utils.logger import setup_logger

def main():
    # 获取 bot 名称
    bot_name = os.environ.get("BOT_NAME", "default")
    
    # 设置日志
    logger = setup_logger(bot_name)
    logger.info(f"Starting bot: {bot_name}")
    
    try:
        # 创建并运行机器人
        bot = ChatBot()
        bot.run()
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()