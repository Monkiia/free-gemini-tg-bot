from .bot import ChatBot
from .config import Config

def main():
    # 验证配置
    Config.validate()
    
    # 创建并运行bot
    bot = ChatBot()
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Bot stopped due to error: {e}")

if __name__ == "__main__":
    main()