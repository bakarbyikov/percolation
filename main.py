import tkinter as tk

from grid import Grid
from instruments import Instruments
from painter import Painter
from settings import *


class App(tk.Frame):

    def __init__(self, parent, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.grid = Grid()

        self.painter = Painter(self, self.grid)
        self.instruments = Instruments(self, self.painter, self.grid)

        self.painter.pack(side=tk.LEFT)
        self.instruments.pack(side=tk.RIGHT, fill='y')
        

if __name__ == "__main__":
    root = tk.Tk()
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()