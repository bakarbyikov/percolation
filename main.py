import tkinter as tk
from random import choices
from time import perf_counter
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from grid import Grid, Link, Node
from settings import *


class Painter:

    def __init__(self, grid: Grid=None) -> None:
        self.probability = PROBABILITY
        self.grid_size = SIZE

        if grid is None:
            self.create_grid()
        else:
            self.grid = grid

        self.root = tk.Tk()
        self.root.bind('<Button-1>', self.on_left_mouse)
        self.root.bind('<Button-2>', self.on_middle_mouse)
        self.root.bind('<Button-3>', self.on_right_mouse)
        
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(expand=1, anchor=tk.W)
        self.update_canvas_size()
        self.draw()
    
    def create_grid(self) -> Grid:
        self.grid = Grid(*self.grid_size)
        self.grid.find_clusters()
    
    def update_canvas_size(self) -> None:
        width = (self.grid.width-1) * LINE_LENGHT + PADDING*2
        height = (self.grid.height-1) * LINE_LENGHT + PADDING*2
        self.canvas.config(width=width, height=height)
    
    def on_left_mouse(self, *args) -> None:
        self.grid_size = choices(range(10, 40), k=2)
        self.create_grid()
        self.update_canvas_size()
        self.update()

    def on_middle_mouse(self, *args) -> None:
        self.grid.find_clusters()
        # print(f'{self.grid.is_leaks() = }')
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
        self.root.mainloop()

def do_experiment(grid: Grid, prob: float, times: int=10**3) -> float:
    n_leaks = 0
    for _ in range(times):
        grid.update(prob)
        n_leaks += grid.is_leaks()
    return n_leaks / times

def do_graph(num: int=31, size: Tuple[int, int]=(10, 10)):
    grid = Grid(*size)
    x = np.linspace(0, 1, num)
    y = list()
    total_time = 0
    for probability in x:
        then = perf_counter()
        leak_percent = do_experiment(grid, probability)
        elapsed = perf_counter() - then
        total_time += elapsed
        y.append(leak_percent)
        print(f"{probability = :0.2f}, {leak_percent = }, {elapsed = }")
    print(f"{total_time = }")
    plt.plot(x, y)
    plt.show()
    

if __name__ == "__main__":
    # do_graph()
    Painter().mainloop()
