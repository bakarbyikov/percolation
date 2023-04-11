import tkinter as tk
import tkinter.ttk as ttk

from instruments import Instruments_panel
from painter import Painter
from plotter import AreaPlot, Sizes_plot
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
        size_plot.pack(fill=tk.BOTH, expand=True)
        
        area_plot = AreaPlot(notebook)
        area_plot.pack(fill=tk.BOTH, expand=True)

        notebook.add(painter, text="Visualizer")
        notebook.add(size_plot, text="Size plot")
        notebook.add(area_plot, text="Area plot")
        

if __name__ == "__main__":
    App().mainloop()