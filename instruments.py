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
        self.width_scale.pack()

        self.height_scale = tk.Scale(self, from_=MIN_GRID, to=MAX_GRID, 
                                      orient=tk.HORIZONTAL,
                                      label='Grid height')
        self.height_scale.set(self.grid.height)
        self.height_scale.bind("<ButtonRelease-1>", self.update_height)
        self.height_scale.pack()

        self.line_lenght = tk.Scale(self, from_=0, to=20, 
                                    orient=tk.HORIZONTAL,
                                    label='Line lenght')
        self.line_lenght.set(self.painter.line_lenght)
        self.line_lenght.bind("<ButtonRelease-1>", self.update_line_lienght)
        self.line_lenght.pack()
        
        self.line_width = tk.Scale(self, from_=0, to=10, 
                                   orient=tk.HORIZONTAL,
                                   label='Line width')
        self.line_width.set(self.painter.line_width)
        self.line_width.bind("<ButtonRelease-1>", self.update_line_width)
        self.line_width.pack()
        
        self.point_radius = tk.Scale(self, from_=0, to=10, 
                                     orient=tk.HORIZONTAL,
                                     label='Line width')
        self.point_radius.set(self.painter.point_radius)
        self.point_radius.bind("<ButtonRelease-1>", self.update_point_radius)
        self.point_radius.pack()

        self.update_button = tk.Button(self, text="Update grid", command=self.update_grid)
        self.update_button.pack(side=tk.BOTTOM)
    
    def update_point_radius(self, *_) -> None:
        self.painter.point_radius = self.point_radius.get()
        self.painter.update_canvas_size()
        self.painter.update()
    def update_line_width(self, *_) -> None:
        self.painter.line_width = self.line_width.get()
        self.painter.update_canvas_size()
        self.painter.update()
    def update_line_lienght(self, *_) -> None:
        self.painter.line_lenght = self.line_lenght.get()
        self.painter.update_canvas_size()
        self.painter.update()
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
