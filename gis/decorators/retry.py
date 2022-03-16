import logging
import math
import time
from functools import wraps


def retry(exception, tries=3, delay=1, back_off=2, logger=None):
    """重试装饰器

    https://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/

    :param exception: 要检查的异常。可能是一个元组
    :param tries: 重试次数
    :param delay: 以秒为单位设置初始延迟
    :param back_off: 等待时长因子
    :param logger: 配置日志器
    """

    if back_off <= 1:
        raise ValueError("backoff must be greater than 1")

    tries = math.floor(tries)
    if tries < 0:
        raise ValueError("tries must be 0 or greater")

    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    if logger is None:
        logger = logging

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            m_tries, m_delay = tries, delay
            while m_tries > 1:
                try:
                    return f(*args, **kwargs)
                except exception as e:
                    logger.error(f"{e}, Retrying in {m_delay} seconds...")
                    time.sleep(m_delay)
                    m_tries -= 1
                    m_delay *= back_off
            return f(*args, **kwargs)

        return f_retry

    return deco_retry
