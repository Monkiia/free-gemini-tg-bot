"""加密货币相关常量"""

# 加密货币ID映射
CRYPTO_MAP = {
    # 主流币
    "btc": "bitcoin",
    "eth": "ethereum",
    "bnb": "binancecoin",
    "sol": "solana",
    "xrp": "ripple",
    "ada": "cardano",
    "doge": "dogecoin",
    
    # 稳定币
    "usdt": "tether",
    "usdc": "usd-coin",
    "dai": "dai",
    
    # 其他常用币
    "dot": "polkadot",
    "link": "chainlink",
    "uni": "uniswap",
    "matic": "polygon",
    "avax": "avalanche-2",
    
    # 常用别名
    "bitcoin": "bitcoin",
    "ethereum": "ethereum",
    "solana": "solana",
    "ripple": "ripple",
    "cardano": "cardano",
}

# 支持的指标列表
SUPPORTED_INDICATORS = [
    "fear_greed",    # 恐慌贪婪指数
    "rainbow",       # 彩虹图
    "s2f",          # Stock-to-Flow模型
    "pi_cycle",     # Pi周期顶部指标
    "mvrv",         # MVRV Z-Score
    "mining",       # 矿工收入分析
    "all"           # 所有指标
]

# 默认支持完整分析的币种
FULL_ANALYSIS_SUPPORTED = {
    "bitcoin",  # 目前只有比特币支持所有指标
} 