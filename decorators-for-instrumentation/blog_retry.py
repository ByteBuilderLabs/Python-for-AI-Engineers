import functools
import time


def retry(fn):
    @functools.wraps(fn)
    def wrapper(*args):
        for attempt in range(3):
            try:
                return fn(*args)
            except ConnectionError:
                if attempt == 2:
                    raise
                time.sleep(0.2 * 2**attempt)

    return wrapper
