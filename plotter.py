import tkinter as tk
from collections import Counter
from time import perf_counter
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

class Cluster_count(tk.Frame):

    def __init__(self, parent, grid: Grid) -> None:
        super().__init__(parent)
        self.parent = parent
        self.grid = grid
        self.do_plot()
    
    def count_clusters(self) -> dict:
        counter = Counter()
        for cluster in self.grid.clusters_list[1:]:
            counter[len(cluster.nodes)] += 1
        x = sorted(counter.keys())
        y = [counter[i] for i in x]
        x = list(map(str, x))
        return x, y
    
    def do_plot(self) -> None:
        figure = plt.Figure(figsize=(10,5), dpi=100)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, self)
        chart_type.get_tk_widget().pack()
        data = self.count_clusters()
        ax.bar(*data)
        ax.set_title("Number of clusters of each size")
        ax.set_xlabel("Cluster size")
        ax.set_ylabel("Number of clusters")

if __name__ == "__main__":
    grid = Grid()
    root = tk.Tk()
    c = Cluster_count(root, grid)
    c.pack()
    root.mainloop()