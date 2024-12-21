import os
from dotenv import load_dotenv

# 从环境变量获取.env文件路径
env_file = os.getenv('ENV_FILE', '.env')
load_dotenv(env_file)

class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    RESPONSE_PROBABILITY = float(os.getenv("RESPONSE_PROBABILITY", "0.3"))
    
    @classmethod
    def validate(cls):
        if not cls.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN not set in environment")
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in environment")