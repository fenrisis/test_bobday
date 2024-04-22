from functools import wraps
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def log_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Starting {func.__name__}")
        result = await func(*args, **kwargs)
        logger.info(f"Completed {func.__name__}")
        return result
    return wrapper
