import tkinter as tk
import tkinter.ttk as ttk

from instruments import Instruments_panel
from painter import Painter
from plotter import AreaPlot, Average_size, Distr_per_prob, Sizes_plot, Cluster_sizes, Cluster_sizes_log
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
        notebook.add(painter, text="Visualizer")

        size_plot = Sizes_plot(notebook)
        size_plot.open("plots/Sizes_plot.npy")
        size_plot.pack(fill=tk.BOTH, expand=True)
        notebook.add(size_plot, text="Size plot")
        
        cluster_sizes = Cluster_sizes(notebook)
        cluster_sizes.open("plots/Clusters_size_plot.npy")
        cluster_sizes.pack(fill=tk.BOTH, expand=True)
        notebook.add(cluster_sizes, text="Cluster sizes")

        cluster_sizes_log = Cluster_sizes_log(notebook)
        cluster_sizes_log.open("plots/Clusters_size_plot.npy")
        cluster_sizes_log.pack(fill=tk.BOTH, expand=True)
        notebook.add(cluster_sizes_log, text="Cluster sizes log")

        average_size = Average_size(notebook)
        average_size.open("plots/Average_size_plot.npy")
        average_size.pack(fill=tk.BOTH, expand=True)
        notebook.add(average_size, text="Average size")
        
        average_size_small = Average_size(notebook)
        average_size_small.open("plots/Average_size_small_plot.npy")
        average_size_small.pack(fill=tk.BOTH, expand=True)
        notebook.add(average_size_small, text="Average size small")
        
        distr_per_prob = Distr_per_prob(notebook)
        distr_per_prob.open("plots/Distr_per_prob_plot.npy")
        distr_per_prob.pack(fill=tk.BOTH, expand=True)
        notebook.add(distr_per_prob, text="Cluster size per prob")
        

if __name__ == "__main__":
    App().mainloop()