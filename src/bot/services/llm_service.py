from openai import OpenAI
from ..config import Config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    async def get_response(self, message: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个群聊机器人，要简短有趣地回复"},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            raise