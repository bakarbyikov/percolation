from functools import wraps
from time import perf_counter
from typing import Any, Callable

from settings import *

def print_elapsed_time(func: Callable) -> Callable:
    @wraps(func)
    def inner(*args, **kwargs) -> Any:
        then = perf_counter()
        res = func(*args, **kwargs)
        elapsed = perf_counter() - then
        if PRINT_ELAPSED_TIME:
            print(f"{func.__qualname__}: {elapsed = }")
        return res
    return inner
