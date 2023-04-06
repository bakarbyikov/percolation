import tkinter as tk
from tkinter import ttk
from collections import Counter

from grid import Cluster, Grid
from plotter import BasePlotter


class Cluster_info(tk.Toplevel):

    def __init__(self, parent, cluster: Cluster) -> None:
        super().__init__(parent)
        self.title("Percolation - Cluster Info")
        self.cluster = cluster

        center_of_mass = tuple(round(i, 3) for i in self.cluster.center_of_mass)
        info = {"Name": self.cluster.name,
                "Area": self.cluster.area,
                "Center of mass": center_of_mass,
                "Radius": self.cluster.radius}
        
        for i, (title, value) in enumerate(info.items()):
            ttk.Label(self, text=str(title)+':', font=('Helvetica', 12))\
                .grid(column=0, row=i,
                      sticky=tk.W,
                      pady=(0, 10))
            ttk.Label(self, text=str(value), font=('Helvetica', 12))\
                .grid(column=1, row=i,
                      sticky=tk.W, 
                      pady=(0, 10))


class Cluster_count(BasePlotter):

    def __init__(self, parent, grid: Grid) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("Percolation - Analyse")
        self.grid = grid
        self.update()
        
    def count_clusters(self) -> dict:
        counter = Counter()
        for cluster in self.grid.clusters_list[1:]:
            counter[len(cluster.nodes)] += 1
        x = sorted(counter.keys())[:30]
        y = [counter[i] for i in x]
        x = list(map(str, x))
        return x, y
    
    def create_axes(self) -> None:
        self.axes = self.figure.add_subplot()
    
    def set_labels(self) -> None:
        self.axes.set_title("Number of clusters of each size")
        self.axes.set_xlabel("Cluster size")
        self.axes.set_ylabel("Number of clusters")
        self.axes.tick_params(axis='x', labelrotation=45)

    def set_data(self) -> None:
        data = self.count_clusters()
        self.axes.bar(*data)

