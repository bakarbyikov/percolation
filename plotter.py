import tkinter as tk
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tqdm import tqdm

from grid import Grid


def leakage_chance(grid: Grid, times: int=10**4) -> float:
    n_leaks = 0
    for _ in range(times):
        grid.update()
        n_leaks += grid.is_leaks()
    return n_leaks / times

def one_test(sizes, prob_points, grid, data, i):
    for y, s in enumerate(sizes):
        grid.change_size(s, s)
        for x, p in enumerate(prob_points):
            grid.change_probability(p)
            grid.update()
            data[x, y, i] = grid.is_leaks()


def do_graph(num: int=20):
    grid = Grid(find_all_clusters=False, update_on_init=False, update_on_changes=False)

    power = 2
    sizes = np.arange(2, 20)
    prob_points = np.linspace(1, 0, num//2, endpoint=False)**power / 2 + 0.5
    prob_points = np.concatenate((prob_points, -np.flip(prob_points)+1))
    prob_points = np.flip(prob_points)
    print(prob_points)
    data = np.full((*prob_points.shape, *sizes.shape, 10**4), float('nan'))
        
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(projection='3d')
    X, Y = np.meshgrid(sizes, prob_points)

    for i in tqdm(range(10**3)):
        for y, s in enumerate(sizes):
            grid.change_size(s, s)
            for x, p in enumerate(prob_points):
                grid.change_probability(p)
                grid.update()
                data[x, y, i] = grid.is_leaks()
    Z = np.nanmean(data, axis=2)
    ax1.clear()
    ax1.plot_surface(X, Y, Z)
    plt.show()


class Cluster_count(tk.Toplevel):

    def __init__(self, parent, grid: Grid) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("Percolation - Analyse")
        self.grid = grid
        
        figure = plt.Figure(figsize=(6,3), dpi=100)
        figure.subplots_adjust(bottom=0.2)
        chart_type = FigureCanvasTkAgg(figure, self)
        chart_type.get_tk_widget().pack()

        self.ax = figure.add_subplot()

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
        self.ax.set_title("Number of clusters of each size")
        self.ax.set_xlabel("Cluster size")
        self.ax.set_ylabel("Number of clusters")
        data = self.count_clusters()
        self.ax.bar(*data)
        self.ax.figure.canvas.draw_idle()


if __name__ == "__main__":
    do_graph()