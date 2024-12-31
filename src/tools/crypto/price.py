from typing import Optional, Type
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
import aiohttp

class CryptoPriceInput(BaseModel):
    """加密货币价格查询的输入参数"""
    crypto_id: str = Field(
        description="加密货币的ID或简写，例如：bitcoin、btc、ethereum、eth"
    )

class CryptoPriceTool(BaseTool):
    name: str = "crypto_price"
    description: str = "获取加密货币的当前价格。输入货币ID（如 bitcoin, ethereum）"
    args_schema: Type[BaseModel] = CryptoPriceInput
    return_direct: bool = True

    async def _arun(self, crypto_id: str) -> str:
        """获取加密货币的当前价格"""
        # 标准化输入
        crypto_id = crypto_id.lower().strip()
        # 处理常见缩写
        crypto_map = {
            "btc": "bitcoin",
            "eth": "ethereum",
            "usdt": "tether",
            "bnb": "binancecoin",
        }
        crypto_id = crypto_map.get(crypto_id, crypto_id)
        
        async with aiohttp.ClientSession() as session:
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": crypto_id,
                "vs_currencies": "usd"
            }
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if crypto_id in data:
                        price = data[crypto_id]['usd']
                        return f"{crypto_id.upper()} 当前价格: ${price:,.2f} USD"
                    return f"找不到 {crypto_id} 的价格信息"
                return f"获取价格时出错: {response.status}"

    def _run(self, crypto_id: str) -> str:
        """同步版本 - 不实现"""
        raise NotImplementedError("请使用异步版本") 