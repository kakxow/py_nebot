from __future__ import annotations
from datetime import datetime as dt

from .nechat_types import Chat


class Tag:
    tag: str
    description: str
    aliases: str





Chats = dict[str, Chat]



def is_cache_timed_out(ts: float, cache_timeout: int) -> bool:
    return dt.now().timestamp() - ts > cache_timeout


def cache(fn, cache_timeout: int = 3600):
    cached_value = None
    ts = dt.now().timestamp()

    def wrapper(*args, **kwargs):
        nonlocal cached_value
        nonlocal ts
        if not cached_value or is_cache_timed_out(ts, cache_timeout):
            ts = dt.now().timestamp()
            cached_value = fn()
        return cached_value
