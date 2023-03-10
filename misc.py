from time import perf_counter
from typing import Tuple

from settings import *

def color_from_rgb(rgb: Tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


class print_elapsed_time:
    def __init__(self, promt: str) -> None:
        print(promt)
        
    def __enter__(self) -> None:
        self.then = perf_counter()
    
    def __exit__(self, *_) -> None:
        elapsed = perf_counter() - self.then
        print(f"{elapsed = }")
