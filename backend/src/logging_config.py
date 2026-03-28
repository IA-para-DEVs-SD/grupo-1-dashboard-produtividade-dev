import sys
import uuid

from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {extra[cid]} | {message}",
    level="INFO",
)


def get_correlation_id() -> str:
    return uuid.uuid4().hex[:8]
