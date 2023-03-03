import tkinter as tk

from grid import Grid
from painter import Painter


class Instruments(tk.Frame):

    def __init__(self, parent: tk.Frame, painter: Painter, grid: Grid) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.painter = painter
        self.grid = grid