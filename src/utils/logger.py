import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(bot_name: str):
    """设置日志记录器"""
    # 创建日志目录
    log_dir = Path("logs") / bot_name
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "bot.log"

    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 设置文件处理器
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # 设置控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger 