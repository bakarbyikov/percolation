import tkinter as tk
from random import choices

import numpy as np

from grid import Grid, Link, Node
from settings import *

class Painter(tk.Frame):

    def __init__(self, parent: tk.Frame, grid: Grid) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.grid = grid
        
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=1, anchor=tk.W)
        self.update_canvas_size()
        self.draw()
        
        self.canvas.bind('<Button-1>', self.on_left_mouse)
        self.canvas.bind('<Button-2>', self.on_middle_mouse)
        self.canvas.bind('<Button-3>', self.on_right_mouse)
    
    def update_canvas_size(self) -> None:
        width = (self.grid.width-1) * LINE_LENGHT + PADDING*2
        height = (self.grid.height-1) * LINE_LENGHT + PADDING*2
        self.canvas.config(width=width, height=height)

    def on_left_mouse(self, *args) -> None:
        size = choices(range(10, 40), k=2)
        self.grid.change_size(*size)
        self.update_canvas_size()
        self.update()

    def on_middle_mouse(self, *args) -> None:
        self.grid.find_clusters()
        self.update()
    
    def on_right_mouse(self, *args) -> None:
        self.grid.update()
        self.grid.find_clusters()
        self.update()
    
    def update(self) -> None:
        self.canvas.delete("all")
        self.draw()

    def draw_point(self, point: Node) -> None:
        coords = np.array(point.coords)
        coords *= LINE_LENGHT
        coords += PADDING
        x, y = coords
        r = POINT_RADIUS
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=point.color)

    def draw_line(self, line: Link) -> None:
        coords = np.array(line.coords)
        coords *= LINE_LENGHT
        coords += PADDING
        self.canvas.create_line(*coords, width=LINE_WIDTH, fill=line.color)
    
    def draw(self):
        for point in self.grid.nodes_list():
            self.draw_point(point)
        for line in self.grid.links_list():
            self.draw_line(line)
    
    def mainloop(self):
        self.parent.mainloop()