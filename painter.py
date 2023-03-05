import tkinter as tk
from random import choices

import numpy as np

from grid import Grid, Link, Node
from misc import print_elapsed_time
from settings import *


class Painter(tk.Frame):

    def __init__(self, parent: tk.Frame, grid: Grid) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.grid = grid

        self.line_lenght = LINE_LENGHT
        self.line_width = LINE_WIDTH
        self.padding = PADDING
        self.point_radius = POINT_RADIUS
        
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack()
        self.update()
        
        self.canvas.bind('<Button-1>', self.on_left_mouse)
        self.canvas.bind('<Button-2>', self.on_middle_mouse)
        self.canvas.bind('<Button-3>', self.on_right_mouse)
    
    def update_canvas_size(self) -> None:
        self.offset = self.padding + max(self.line_width, self.point_radius)
        self.width = (self.grid.width-1) * self.line_lenght + self.offset*2
        self.height = (self.grid.height-1) * self.line_lenght + self.offset*2
        self.canvas.config(width=self.width, height=self.height)

    def on_middle_mouse(self, *_) -> None:
        size = choices(range(10, 40), k=2)
        self.grid.change_size(*size, find_clusters=True)
        self.update()

    def on_right_mouse(self, *_) -> None:
        self.grid.find_clusters()
        self.update(size_changed=False)
    
    def on_left_mouse(self, *_) -> None:
        self.grid.update(True)
        self.update(size_changed=False)
    
    @print_elapsed_time
    def update(self, size_changed: bool=True) -> None:
        if size_changed:
            self.update_canvas_size()
        self.canvas.delete("all")
        self.draw()

    def draw_point(self, point: Node) -> None:
        coords = np.array(point.coords)
        coords *= self.line_lenght
        coords += self.offset
        x, y = coords
        r = self.point_radius
        self.canvas.create_oval(x-r, y-r, x+r-1, y+r-1, fill=point.color, outline='')

    def draw_line(self, line: Link) -> None:
        coords = np.array(line.coords)
        coords *= self.line_lenght
        coords += self.offset
        self.canvas.create_line(*coords, width=self.line_width, fill=line.color)
    
    def draw(self):
        for point in self.grid.nodes_list():
            self.draw_point(point)
        for line in self.grid.links_list():
            self.draw_line(line)


if __name__ == '__main__':
    root = tk.Tk()
    painter = Painter(root, Grid())
    painter.pack()
    root.mainloop()