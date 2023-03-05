from functools import wraps
from time import perf_counter
from typing import Any, Callable, ParamSpec, TypeVar

from settings import *

P = ParamSpec("P")
R = TypeVar("R")

def print_elapsed_time(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        then = perf_counter()
        res = func(*args, **kwargs)
        elapsed = perf_counter() - then
        if PRINT_ELAPSED_TIME:
            print(f"{func.__qualname__}: {elapsed = }")
        return res
    return inner
