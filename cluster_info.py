import tkinter as tk
from tkinter import ttk
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from grid import Cluster, Grid


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
        x = sorted(counter.keys())[:30]
        y = [counter[i] for i in x]
        x = list(map(str, x))
        return x, y
    
    def update(self) -> None:
        self.ax.clear()
        self.ax.set_title("Number of clusters of each size")
        self.ax.set_xlabel("Cluster size")
        self.ax.set_ylabel("Number of clusters")
        self.ax.tick_params(axis='x', labelrotation=45)
        data = self.count_clusters()
        self.ax.bar(*data)
        self.ax.figure.canvas.draw_idle()

