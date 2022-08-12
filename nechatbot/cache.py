from datetime import datetime as dt
from functools import wraps


def is_cache_timed_out(ts: float, cache_timeout: int) -> bool:
    return dt.now().timestamp() - ts > cache_timeout


def cache(cache_timeout: int = 3600):
    def wrapper_fn(fn):
        cached_value = None
        ts = dt.now().timestamp()

        @wraps(fn)
        def wrapper(*args, **kwargs):
            nonlocal cached_value
            nonlocal ts

            if not cached_value or is_cache_timed_out(ts, cache_timeout):
                ts = dt.now().timestamp()
                cached_value = fn(*args, **kwargs)
            return cached_value

        def update_cache(value):
            nonlocal cached_value
            nonlocal ts
            cached_value = value
            ts = dt.now().timestamp()

        setattr(wrapper, "update_cache", update_cache)
        return wrapper

    return wrapper_fn
