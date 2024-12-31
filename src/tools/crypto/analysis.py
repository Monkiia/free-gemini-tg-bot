from typing import Optional, Type, List, Union
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
import aiohttp
from datetime import datetime, timedelta
from .constants import CRYPTO_MAP, SUPPORTED_INDICATORS, FULL_ANALYSIS_SUPPORTED

class CryptoAnalysisInput(BaseModel):
    """加密货币技术分析的输入参数"""
    crypto_id: Union[str, dict] = Field(
        description="加密货币的ID或简写，例如：bitcoin、btc"
    )
    indicators: List[str] = Field(
        default=["all"],
        description=f"要分析的指标，可选：{', '.join(SUPPORTED_INDICATORS)}"
    )

class CryptoAnalysisTool(BaseTool):
    name: str = "crypto_analysis"
    description: str = """分析加密货币的技术指标和市场情绪。
可分析的指标包括：
- Fear & Greed Index (恐慌指数)
- Rainbow Price Chart (彩虹图)
- Stock-to-Flow Model (S2F模型)
- Pi Cycle Top Indicator (Pi周期顶部指标)
- MVRV Z-Score (市值实现值Z评分)
- Mining Analysis (矿工收入分析)
"""
    args_schema: Type[BaseModel] = CryptoAnalysisInput
    return_direct: bool = True

    async def _arun(self, crypto_id: Union[str, dict], indicators: List[str] = ["all"]) -> str:
        """分析加密货币的技术指标"""
        # 处理输入格式
        if isinstance(crypto_id, dict):
            crypto_id = str(crypto_id).strip('{}').strip()
        else:
            crypto_id = str(crypto_id).strip()

        # 标准化输入
        crypto_id = crypto_id.lower()
        crypto_id = CRYPTO_MAP.get(crypto_id, crypto_id)

        # 检查是否支持完整分析
        if crypto_id not in FULL_ANALYSIS_SUPPORTED and "all" in indicators:
            print(f"警告：{crypto_id} 不支持所有指标，只支持恐惧贪婪指数")
            indicators = ["fear_greed"]

        analysis_results = []
        
        async with aiohttp.ClientSession() as session:
            # 获取恐慌指数
            if "all" in indicators or "fear_greed" in indicators:
                fear_greed = await self._get_fear_greed_index(session)
                if fear_greed:
                    analysis_results.append(fear_greed)

            if crypto_id in FULL_ANALYSIS_SUPPORTED:
                # 比特币特有指标
                if "all" in indicators or "rainbow" in indicators:
                    rainbow = await self._get_rainbow_chart(session)
                    if rainbow:
                        analysis_results.append(rainbow)

                if "all" in indicators or "s2f" in indicators:
                    s2f = await self._get_stock_to_flow(session)
                    if s2f:
                        analysis_results.append(s2f)

                if "all" in indicators or "mvrv" in indicators:
                    mvrv = await self._get_mvrv_zscore(session)
                    if mvrv:
                        analysis_results.append(mvrv)

                if "all" in indicators or "mining" in indicators:
                    mining = await self._get_mining_analysis(session)
                    if mining:
                        analysis_results.append(mining)

        if not analysis_results:
            return f"抱歉，无法获取 {crypto_id} 的技术分析数据。"

        return "\n\n".join([
            f"📊 {crypto_id.upper()} 技术分析报告",
            *analysis_results
        ])

    async def _get_fear_greed_index(self, session: aiohttp.ClientSession) -> Optional[str]:
        """获取恐慧指数"""
        try:
            url = "https://api.alternative.me/fng/"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    value = int(data['data'][0]['value'])
                    classification = self._classify_fear_greed(value)
                    return f"😱 恐慌贪婪指数: {value} - {classification}"
        except Exception as e:
            print(f"Error getting fear & greed index: {e}")
        return None

    async def _get_rainbow_chart(self, session: aiohttp.ClientSession) -> Optional[str]:
        """获取彩虹图分析"""
        try:
            url = "https://api.blockchain.info/charts/market-price"
            params = {
                "timespan": "30days",
                "format": "json"
            }
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    current_price = data['values'][-1]['y']
                    analysis = self._analyze_rainbow_price(current_price)
                    return f"🌈 彩虹图分析: {analysis}"
        except Exception as e:
            print(f"Error getting rainbow chart: {e}")
        return None

    async def _get_stock_to_flow(self, session: aiohttp.ClientSession) -> Optional[str]:
        """获取S2F模型分析"""
        try:
            # 这里应该调用实际的S2F API
            # 目前返回模拟数据
            return "📈 S2F模型分析: 当前价格处于模型预测范围的下方，可能被低估"
        except Exception as e:
            print(f"Error getting S2F analysis: {e}")
        return None

    async def _get_mvrv_zscore(self, session: aiohttp.ClientSession) -> Optional[str]:
        """获取MVRV Z-Score分析"""
        try:
            # 这里应该调用实际的MVRV API
            # 目前返回模拟数据
            return "📊 MVRV Z-Score: 2.1 - 市场估值适中，未到极端区域"
        except Exception as e:
            print(f"Error getting MVRV Z-Score: {e}")
        return None

    async def _get_mining_analysis(self, session: aiohttp.ClientSession) -> Optional[str]:
        """获取矿工收入分析"""
        try:
            # 这里应该调用实际的矿工数据API
            # 目前返回模拟数据
            return "⛏️ 矿工收入分析: 矿工收入稳定，哈希率处于历史高位"
        except Exception as e:
            print(f"Error getting mining analysis: {e}")
        return None

    def _classify_fear_greed(self, value: int) -> str:
        """将恐慌贪婪指数分类"""
        if value <= 20:
            return "极度恐慌"
        elif value <= 40:
            return "恐慌"
        elif value <= 60:
            return "中性"
        elif value <= 80:
            return "贪婪"
        else:
            return "极度贪婪"

    def _analyze_rainbow_price(self, price: float) -> str:
        """分析彩虹图位置"""
        # 这里应该有更复杂的彩虹图计算逻辑
        if price < 30000:
            return "价格处于'极度低估'区域"
        elif price < 50000:
            return "价格处于'低估'区域"
        else:
            return "价格处于'合理'区域"

    def _run(self, crypto_id: str, indicators: List[str] = ["all"]) -> str:
        """同步版本 - 不实现"""
        raise NotImplementedError("请使用异步版本") 