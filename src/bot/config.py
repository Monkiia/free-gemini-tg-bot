import os
from pathlib import Path
from dotenv import load_dotenv

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 尝试多个可能的 .env 文件位置
ENV_PATHS = [
    os.getenv('ENV_FILE'),  # 首先检查环境变量中指定的路径
    Path(__file__).parent / '.env',  # src/bot/.env
    PROJECT_ROOT / '.env',  # 项目根目录的 .env
    PROJECT_ROOT / 'config' / '.env'  # config/.env
]

# 加载找到的第一个 .env 文件
for env_path in ENV_PATHS:
    if env_path and Path(env_path).is_file():
        load_dotenv(env_path)
        print(f"Loaded environment from: {env_path}")
        break

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    RESPONSE_PROBABILITY = float(os.getenv("RESPONSE_PROBABILITY", "0.3"))
    
    @classmethod
    def validate(cls):
        missing = []
        if not cls.TELEGRAM_TOKEN:
            missing.append("TELEGRAM_TOKEN")
        if not cls.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
            
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
            
        # 验证 API key 格式
        if not cls.GEMINI_API_KEY.startswith("AI"):
            print("Warning: GEMINI_API_KEY format looks incorrect")
            
        print("Configuration validated successfully")
        print(f"Using Telegram Bot Token: {cls.TELEGRAM_TOKEN[:10]}...")
        print(f"Using Gemini API Key: {cls.GEMINI_API_KEY[:10]}...")
        print(f"Response Probability: {cls.RESPONSE_PROBABILITY}")