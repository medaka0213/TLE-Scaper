import logging
import time
import functools

logger = logging.getLogger(__name__)


def retry(
    max_retry=3,
    retry_interval=1,
    retry_on=None,
    retry_on_exception=None,
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
                    if retry_on_exception and not retry_on_exception(e):
                        raise e
                    if retry_on and not retry_on(e):
                        raise e
                    logger.log(
                        log_level,
                        f"An error occurred while executing {func.__name__}",
                        exc_info=e,
                    )
                    logger.info(f"Retry {i+1}/{max_retry} in {retry_interval} seconds")
                    time.sleep(retry_interval)

        return wrapper

    return decorator
