import tkinter as tk
import tkinter.ttk as ttk

from instruments import Instruments_panel
from painter import Painter
from plotter import AreaPlot, Sizes_plot, Cluster_sizes, Cluster_sizes_log
from settings import *
from visualization import Visualization


class App(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Percolation")
        self.geometry("{0}x{1}".format(*WINDOW_ZISE))
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH)

        painter = Visualization(self)
        painter.pack(fill=tk.BOTH, expand=True)

        size_plot = Sizes_plot(notebook)
        size_plot.open("plots/Sizes_plot.npy")
        size_plot.pack(fill=tk.BOTH, expand=True)
        
        cluster_sizes = Cluster_sizes(notebook)
        cluster_sizes.open("plots/Clusters_size_plot.npy")
        cluster_sizes.pack(fill=tk.BOTH, expand=True)

        cluster_sizes_log = Cluster_sizes_log(notebook)
        cluster_sizes_log.open("plots/Clusters_size_plot.npy")
        cluster_sizes_log.pack(fill=tk.BOTH, expand=True)

        notebook.add(painter, text="Visualizer")
        notebook.add(size_plot, text="Size plot")
        notebook.add(cluster_sizes, text="Cluster sizes")
        notebook.add(cluster_sizes_log, text="Cluster sizes log")
        

if __name__ == "__main__":
    App().mainloop()