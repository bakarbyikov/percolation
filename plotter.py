import tkinter as tk
from collections import Counter
from time import perf_counter
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from grid import Grid


def leakage_chance(grid: Grid, times: int=10**3) -> float:
    n_leaks = 0
    for _ in range(times):
        grid.update()
        n_leaks += grid.is_leaks()
    return n_leaks / times

def do_graph(num: int=31, size: Tuple[int, int]=(20, 20)):
    grid = Grid(*size, find_all_clusters=False, update_on_init=False)
    x = np.linspace(0, 1, num)
    y = list()
    total_time = 0
    for probability in x:
        grid.change_probability(probability)
        then = perf_counter()
        leak_percent = leakage_chance(grid)
        elapsed = perf_counter() - then
        total_time += elapsed
        y.append(leak_percent)
        print(f"{probability = :0.2f}, {leak_percent = }, {elapsed = }")
    print(f"{total_time = }")
    plt.plot(x, y)
    plt.show()

class Cluster_count(tk.Toplevel):

    def __init__(self, parent, grid: Grid) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("Percolation - Analyse")
        self.grid = grid
        
        figure = plt.Figure(figsize=(6,3), dpi=100)
        chart_type = FigureCanvasTkAgg(figure, self)
        chart_type.get_tk_widget().pack()

        self.ax = figure.add_subplot(111)
        self.ax.set_title("Number of clusters of each size")
        self.ax.set_xlabel("Cluster size")
        self.ax.set_ylabel("Number of clusters")

        self.update()
    
    def count_clusters(self) -> dict:
        counter = Counter()
        for cluster in self.grid.clusters_list[1:]:
            counter[len(cluster.nodes)] += 1
        x = sorted(counter.keys())
        y = [counter[i] for i in x]
        x = list(map(str, x))
        return x, y
    
    def update(self) -> None:
        self.ax.clear()
        data = self.count_clusters()
        self.ax.bar(*data)
        self.ax.figure.canvas.draw_idle()


if __name__ == "__main__":
    grid = Grid()
    root = tk.Tk()
    c = Cluster_count(root, grid)
    
    def update_on_click(*_):
        grid.update()
        grid.print()
        c.update()

    root.bind('<Button-1>', update_on_click)
    root.mainloop()

    do_graph()