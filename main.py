
import tkinter as tk
from itertools import product
from random import choices
from secrets import token_hex
from time import perf_counter
from typing import Iterable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

SIZE = WIDTH, HEIGHT = 40, 40
PROBABILITY = 0.5

PADDING = 10
LINE_LENGHT = 20
LINE_WIDTH = 10
POINT_RADIUS = 5

class Cluster:
    def __init__(self, name: int, nodes: Iterable=()) -> None:
        self.name = name
        self.nodes = set(nodes)
        self.color = '#'+token_hex(3)
    
    def add_node(self, x: int, y: int) -> None:
        self.nodes.add((x, y))
    
    def __lt__(self, value: 'Cluster') -> bool:
        return self.name < value.name

class Link:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, cluster: Cluster) -> None:
        self.coords = (x1, y1, x2, y2)
        self.cluster = cluster
        self.color = 'black' if cluster is None else self.cluster.color

class Node:
    def __init__(self, x: int, y: int, cluster: Cluster, r: int=POINT_RADIUS) -> None:
        self.coords = (x, y)
        self.r = r
        self.cluster = cluster
        self.color = 'black' if cluster is None else self.cluster.color
        
class Grid:

    def __init__(self, width: int, height: int) -> None:
        self.size = self.width, self.height = width, height
        self.update()
    
    def update(self, prob: float=PROBABILITY) -> None:
        self.horizontal_links = np.random.rand(self.width, self.height) < prob
        self.horizontal_links[-1, :] = False
        self.vertical_links = np.random.rand(self.width, self.height) < prob
        self.vertical_links[:, -1] = False

        self.clusters = np.empty(self.size, Cluster)
        self.clusters_list = []
    
    def links_list(self) -> List[Link]:
        lines = []
        for x1, y1 in np.argwhere(self.horizontal_links):
            cluster = self.clusters[x1, y1]
            lines.append(Link(x1, y1, x1+1, y1, cluster))
        for x1, y1 in np.argwhere(self.vertical_links):
            cluster = self.clusters[x1, y1]
            lines.append(Link(x1, y1, x1, y1+1, cluster))
        return lines

    def nodes_list(self) -> List[Node]:
        points = []
        for x, y in product(range(self.width), range(self.height)):
            cluster = self.clusters[x, y]
            points.append(Node(x, y, cluster))
        return points
    
    def is_leaks(self) -> bool:
        if len(self.clusters_list) <= 0:
            on_borders = product((0, self.width-1), range(self.height))
            self.find_clusters(set(on_borders))
        clusters_left = self.clusters[0, :]
        clusters_right = self.clusters[-1, :]
        leak = np.intersect1d(clusters_left, clusters_right)
        return leak.size > 0
    
    def DFS(self, start: Tuple[int, int]) -> List[Tuple[int, int]]:
        visited = set((start, ))
        backtrack = [start, ]
        for x, y in backtrack:
            connected = list()
            if x+1 < self.width and self.horizontal_links[x, y]:
                connected.append((x+1, y))
            if y+1 < self.height and self.vertical_links[x, y]:
                connected.append((x, y+1))
            if x > 0 and self.horizontal_links[x-1, y]:
                connected.append((x-1, y))
            if y > 0 and self.vertical_links[x, y-1]:
                connected.append((x, y-1))
            for node in connected:
                if node not in visited:
                    visited.add(node)
                    backtrack.append(node)
        return backtrack
    
    def find_clusters(self, where: set=None):
        if where is None:
            to_visit = set(product(range(self.width), range(self.height)))
        else:
            to_visit = where
            
        while to_visit:
            nodes = self.DFS(to_visit.pop())
            to_visit.difference_update(nodes)
            cluster = Cluster(len(self.clusters_list), nodes)
            self.clusters_list.append(cluster)
            for x, y in nodes:
                self.clusters[x, y] = cluster

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
        r = point.r
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
    do_graph()
    Painter().mainloop()
