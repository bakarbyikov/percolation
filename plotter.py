from time import perf_counter
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from grid import Grid

def do_experiment(grid: Grid, times: int=10**3) -> float:
    n_leaks = 0
    for _ in range(times):
        grid.update()
        n_leaks += grid.is_leaks()
    return n_leaks / times

def do_graph(num: int=31, size: Tuple[int, int]=(10, 10)):
    grid = Grid(*size)
    x = np.linspace(0, 1, num)
    y = list()
    total_time = 0
    for probability in x:
        grid.change_probability(probability)
        then = perf_counter()
        leak_percent = do_experiment(grid)
        elapsed = perf_counter() - then
        total_time += elapsed
        y.append(leak_percent)
        print(f"{probability = :0.2f}, {leak_percent = }, {elapsed = }")
    print(f"{total_time = }")
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    do_graph()