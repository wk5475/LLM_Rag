import time
from functools import wraps
from utils.log import Log
import asyncio

logger = Log()


def timer_decorator(func):
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)  # 同步调用
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        logger.info(f"{func.__name__} 实际用时: {elapsed:.6f}秒")
        return result

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)  # 异步调用
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        logger.info(f"{func.__name__} 实际用时: {elapsed:.6f}秒")
        return result

    # 根据被装饰函数是否为异步，返回对应的包装器
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
