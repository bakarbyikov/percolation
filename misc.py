from time import perf_counter

from settings import *

class print_elapsed_time:
    def __init__(self, promt: str) -> None:
        print(promt)
        
    def __enter__(self) -> None:
        self.then = perf_counter()
    
    def __exit__(self, *_) -> None:
        elapsed = perf_counter() - self.then
        print(f"{elapsed = }")
