import tkinter as tk
from tkinter import ttk
from grid import Cluster

class Cluster_info(tk.Toplevel):

    def __init__(self, parent, cluster: Cluster) -> None:
        super().__init__(parent)
        self.title("Percolation - Cluster Info")
        self.cluster = cluster

        info = {"Name": self.cluster.name,
                "Area": self.cluster.area,
                "Center of mass": self.cluster.center_of_mass,
                "Radius": self.cluster.radius}
        left, right = tk.Frame(self), tk.Frame(self)
        left.pack(side=tk.LEFT)
        right.pack(side=tk.LEFT)
        for title, value in info.items():
            ttk.Label(left, text=str(title)+':').pack( padx=10, anchor=tk.W)
            ttk.Label(right, text=str(value)).pack(padx=10, anchor=tk.W)

