import os

from loguru import logger

from settings import settings
from src.common.constant import Constant

_log_dir = os.path.join(settings.BASE_DIR, "logs")
if not os.path.exists(_log_dir):
    os.mkdir(_log_dir)

logger.add(
    sink=os.path.join(_log_dir, "debug.log"),
    level="DEBUG",
    encoding=Constant.UTF8,
    rotation="1 MB"
)

logger.add(
    sink=os.path.join(_log_dir, "error.log"),
    level="ERROR",
    encoding=Constant.UTF8,
    rotation="1 MB"
)
