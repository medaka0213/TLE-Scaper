import logging
import time
import functools
from typing import List

logger = logging.getLogger(__name__)


def retry(
    max_retry=3,
    retry_interval=1,
    raise_on: List[Exception] = [],
    retry_on: List[Exception] = [],
    log_level=logging.WARNING,
):
    """リトライを追加するためのデコレーター"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retry):
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception as e:
                    if i + 1 == max_retry:
                        # raise if last trial
                        raise e
                    logger.log(
                        log_level,
                        f"An error occurred while executing {func.__name__}",
                        exc_info=e,
                    )

                    if raise_on:
                        for ex in raise_on:
                            if isinstance(e, ex):
                                raise e
                    if retry_on:
                        for ex in retry_on:
                            if isinstance(e, ex):
                                break
                        else:
                            # raise if not retry_on
                            raise e
                    logger.info(f"Retry {i+1}/{max_retry} in {retry_interval} seconds")
                    time.sleep(retry_interval)

        return wrapper

    return decorator
