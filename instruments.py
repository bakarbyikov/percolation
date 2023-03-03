import tkinter as tk

from grid import Grid
from painter import Painter
from settings import *


class Instruments(tk.Frame):

    def __init__(self, parent: tk.Frame, painter: Painter, grid: Grid) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.painter = painter
        self.grid = grid

        self.width_scale = tk.Scale(self, from_=MIN_GRID, to=MAX_GRID, 
                                      orient=tk.HORIZONTAL,
                                      label='Grid width')
        self.width_scale.set(self.grid.width)
        self.width_scale.bind("<ButtonRelease-1>", self.update_width)

        self.height_scale = tk.Scale(self, from_=MIN_GRID, to=MAX_GRID, 
                                      orient=tk.HORIZONTAL,
                                      label='Grid height')
        self.height_scale.set(self.grid.height)
        self.height_scale.bind("<ButtonRelease-1>", self.update_height)
        self.update_button = tk.Button(self, text="Update grid", command=self.update_grid)

        self.width_scale.pack()
        self.height_scale.pack()
        self.update_button.pack(side=tk.BOTTOM)
    
    def update_width(self, event) -> None:
        width = self.width_scale.get()
        height = self.grid.height
        self.update_grid_size(width, height)
    def update_height(self, event) -> None:
        width = self.grid.width
        height = self.height_scale.get()
        self.update_grid_size(width, height)
    
    def update_grid_size(self, width: int, height: int) -> None:
        self.grid.change_size(width, height)
        self.painter.update_canvas_size()
        self.painter.update()
    
    def update_grid(self):
        self.grid.update()
        self.painter.update()
        pass
