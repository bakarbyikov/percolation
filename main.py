import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
from threading import Thread
from typing import Callable

from instruments import Instruments_panel
from painter import Painter
from plotter import AreaPlot, Sizes_plot
from settings import *


class App(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Percolation")
        ttk.Label(self, text="Percolation simulator", 
                  font=('Helvetica', 15)).pack(pady=10, padx=10)
        buttons = ttk.Frame(self)
        buttons.pack(pady=20, padx=20)
        ttk.Button(buttons, text="Grid editor", 
                   command=partial(self.threading, self.open_editor)).pack(pady=5, fill=tk.X)

        ttk.Button(buttons, text="Big plots", 
                   command=self.show_plots).pack(pady=5, fill=tk.X)

        ttk.Button(buttons, text="Area plot", 
                   command=self.show_area_plot).pack(pady=5, fill=tk.X)
    
    def threading(self, target: Callable[[], None]) -> None:
        t = Thread(target=target)
        t.start()
    
    def show_plots(self) -> None:
        plt = Sizes_plot(self)
        plt.open("plots/Sizes_plot.npy")

    def show_area_plot(self) -> None:
        plt = AreaPlot(self)
        plt.open("plots/Area_plot.npy")
    
    def open_editor(self) -> None:
        painter = Painter(self)
        tools = Instruments_panel(painter, painter)
        tools.protocol("WM_DELETE_WINDOW", painter.destroy)

if __name__ == "__main__":
    App().mainloop()