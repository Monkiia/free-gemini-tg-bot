import os
from pathlib import Path
from dotenv import load_dotenv

# 获取配置文件路径
config_dir = Path("config")
env_file = config_dir / ".env"

# 加载环境变量
if env_file.exists():
    load_dotenv(env_file)
else:
    raise FileNotFoundError(f"Environment file not found: {env_file}")

class Config:
    """配置类"""
    
    # Telegram 配置
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN not found in environment variables")
    
    # Gemini 配置
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    # 机器人配置
    RESPONSE_PROBABILITY = os.getenv("RESPONSE_PROBABILITY", "0.3")
    BOT_NAME = os.getenv("BOT_NAME", "default")
    
    @classmethod
    def validate(cls):
        """验证配置"""
        required_vars = [
            ("TELEGRAM_TOKEN", cls.TELEGRAM_TOKEN),
            ("GEMINI_API_KEY", cls.GEMINI_API_KEY),
        ]
        
        missing = [var for var, val in required_vars if not val]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")