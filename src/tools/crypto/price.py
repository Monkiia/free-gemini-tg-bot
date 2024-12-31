from typing import Optional, Type
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
import aiohttp
import asyncio
from .constants import CRYPTO_MAP

class CryptoPriceInput(BaseModel):
    """加密货币价格查询的输入参数"""
    crypto_id: str = Field(
        description="加密货币的ID或简写，例如：bitcoin、btc"
    )

class CryptoPriceTool(BaseTool):
    name: str = "crypto_price"
    description: str = "查询加密货币的当前价格"
    args_schema: Type[BaseModel] = CryptoPriceInput
    return_direct: bool = True

    async def _arun(self, crypto_id: str) -> str:
        """查询加密货币价格"""
        # 标准化输入
        crypto_id = crypto_id.lower().strip()
        crypto_id = CRYPTO_MAP.get(crypto_id, crypto_id)

        # 最大重试次数
        max_retries = 3
        retry_delay = 1  # 秒

        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    # 添加请求头和超时设置
                    headers = {
                        "Accept": "application/json",
                        "User-Agent": "Mozilla/5.0"
                    }
                    timeout = aiohttp.ClientTimeout(total=10)
                    
                    url = "https://api.coingecko.com/api/v3/simple/price"
                    params = {
                        "ids": crypto_id,
                        "vs_currencies": "usd"
                    }

                    async with session.get(
                        url, 
                        params=params, 
                        headers=headers,
                        timeout=timeout
                    ) as response:
                        # 处理API限制
                        if response.status == 429:  # Too Many Requests
                            if attempt < max_retries - 1:
                                await asyncio.sleep(retry_delay * (attempt + 1))
                                continue
                            return "抱歉，API 请求次数已达上限，请稍后再试"

                        # 处理其他HTTP错误
                        if response.status != 200:
                            error_msg = await response.text()
                            print(f"API Error: Status {response.status}, {error_msg}")
                            return f"获取 {crypto_id} 价格失败，请稍后再试"

                        try:
                            data = await response.json()
                        except Exception as e:
                            print(f"JSON decode error: {e}")
                            return f"解析 {crypto_id} 价格数据失败"

                        if not data:
                            return f"未收到 {crypto_id} 的价格数据"

                        if crypto_id in data:
                            try:
                                price = data[crypto_id]["usd"]
                                return f"{crypto_id.upper()} 当前价格: ${price:,.2f} USD"
                            except (KeyError, TypeError) as e:
                                print(f"Price data format error: {e}")
                                return f"价格数据格式错误: {crypto_id}"
                        return f"未找到 {crypto_id} 的价格信息"

            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                return f"查询 {crypto_id} 价格超时，请稍后再试"

            except Exception as e:
                print(f"Error getting crypto price: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                return f"查询 {crypto_id} 价格时出错，请稍后再试"

    def _run(self, crypto_id: str) -> str:
        """同步版本 - 不实现"""
        raise NotImplementedError("请使用异步版本") 