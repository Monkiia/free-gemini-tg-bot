import asyncio
import signal
from .bot import ChatBot
from .config import Config

async def main():
    # 验证配置
    Config.validate()
    
    # 创建bot
    bot = ChatBot()
    
    # 设置信号处理
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    
    def signal_handler():
        print("\nReceived stop signal")
        stop_event.set()
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        # 启动bot
        await bot.start()
        
        # 等待停止信号
        await stop_event.wait()
        
    except Exception as e:
        print(f"Bot stopped due to error: {e}")
    finally:
        if bot.running:
            print("Shutting down...")
            await bot.stop()

def run():
    """运行bot的主入口"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")

if __name__ == "__main__":
    run()