from functools import cached_property, reduce
from itertools import compress, product
from math import pi, sqrt
from typing import List, Set, Tuple

import numpy as np
from tqdm import tqdm

from settings import *


class Cluster:
    def __init__(self, name: int, nodes: set) -> None:
        self.name = name
        self.nodes = nodes

    @cached_property
    def center_of_mass(self) -> Tuple[float, float]:
        x, y = reduce(lambda x, y: (x[0]+y[0], x[1]+y[1]), self.nodes)
        x, y = x/self.size, y/self.size
        return x, y
    
    @cached_property
    def radius(self) -> float:
        return sqrt(self.area / pi)

    @cached_property
    def area(self) -> int:
        return self.size

    @cached_property
    def size(self) -> int:
        return len(self.nodes)

class Grid:

    def __init__(self, width: int=WIDTH, height: int=HEIGHT, 
                 prob: float=PROBABILITY, find_all_clusters=True,
                 update_on_changes=True, update_on_init=True) -> None:
        self.size = self.width, self.height = width, height
        self.prob = prob
        self.find_all_clusters = find_all_clusters
        self.update_on_changes = update_on_changes

        self.horizontal_links = np.zeros(self.size, bool)
        self.vertical_links = np.zeros(self.size, bool)

        self.clusters = np.zeros(self.size, np.uint32)
        self.clusters_list = [None, ]

        if update_on_init:
            self.update()
    
    def flood(self) -> None:
        self.horizontal_links = np.random.binomial(1, self.prob, self.size)
        self.vertical_links = np.random.binomial(1, self.prob, self.size)
        self.horizontal_links[-1, :] = False
        self.vertical_links[:, -1] = False

    def forget_clusters(self) -> None:
        self.clusters = np.zeros(self.size, np.uint32)
        self.clusters_list = [None, ]
    
    def update(self) -> None:
        self.flood()
        self.forget_clusters()
        if self.find_all_clusters:
            self.find_clusters()
    
    def change_size(self, width: int=None, height: int=None) -> None:
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        self.size = self.width, self.height
        if self.update_on_changes:
            self.update()
    
    def change_probability(self, prob: float) -> None:
        self.prob = prob
        if self.update_on_changes:
            self.update()
    
    def is_leaks(self) -> bool:
        on_left_border = product((0, ), range(self.height))
        to_visit = set(on_left_border)
        
        while to_visit:
            leaks, nodes = self.is_cluster_leaks(to_visit.pop())
            if leaks:
                return True
            to_visit.difference_update(nodes)
        return False
    
    def is_cluster_leaks(self, start: Tuple[int, int]) -> Tuple[bool, set]:
        visited = set((start, ))
        backtrack = [start, ]
        while backtrack:
            x, y = backtrack.pop()
            connected = self.find_connected(x, y)
            if not connected:
                continue
            if connected[-1][0] == self.width-1:
                visited.add(connected[-1])
                return True, visited
            for node in connected:
                if node not in visited:
                    visited.add(node)
                    backtrack.append(node)
        return False, visited

    def find_connected(self, x: int, y: int) -> List[Tuple[int, int]]:
        connected = list()
        # Left
        if self.horizontal_links[x-1, y]:
            connected.append((x-1, y))
        # Bottom
        if self.vertical_links[x, y]:
            connected.append((x, y+1))
        # Top
        if self.vertical_links[x, y-1]:
            connected.append((x, y-1))
        # Right
        if self.horizontal_links[x, y]:
            connected.append((x+1, y))

        return connected
    
    def DFS(self, start: Tuple[int, int]) -> Set[Tuple[int, int]]:
        visited = set((start, ))
        backtrack = [start, ]
        while backtrack:
            x, y = backtrack.pop()
            for node in self.find_connected(x, y):
                if node not in visited:
                    visited.add(node)
                    backtrack.append(node)
        return visited
    
    def find_clusters(self):
        to_visit = set(product(range(self.width), range(self.height)))  
        
        while to_visit:
            nodes = self.DFS(to_visit.pop())
            to_visit.difference_update(nodes)
            cluster = Cluster(len(self.clusters_list), nodes)
            self.clusters_list.append(cluster)
            for x, y in nodes:
                self.clusters[x, y] = cluster.name
    
    def get_cluster_on(self, x: int, y: int) -> Cluster:
        return self.clusters_list[self.clusters[x, y]]
    
    def print(self) -> str:
        symbols = str.maketrans({'0':'▘ ', '1':'▀▀', '2':'▌ ', '3':'▛▀'})
        print(self.to_text().translate(symbols))
    
    def to_text(self) -> str:
        rows_list = []
        for y in range(self.height):
            rows_list.append([])
            for x in range(self.width):
                i = self.horizontal_links[x, y] + self.vertical_links[x, y]*2
                rows_list[-1].append(str(i))
            rows_list[-1] = ''.join(rows_list[-1])
        text = '\n'.join(rows_list)
        return text
    
    @classmethod
    def from_text(cls, text: str) -> 'Grid':
        w, h = text.find('\n'), text.count('\n')+1
        print(f"{w, h = }")
        grid = Grid(w, h, update_on_init=False)
        for y, row in enumerate(text.splitlines()):
            for x, cell in enumerate(row):
                if cell in ('1', '3'):
                    grid.horizontal_links[x, y] = True
                if cell in ('2', '3'):
                    grid.vertical_links[x, y] = True
        return grid

if __name__ == '__main__':
    from perf_measurer import count_time
    w, h = 1000, 1000
    grid = Grid(w, h, find_all_clusters=False, update_on_init=False)

    with count_time() as timer:
        grid.is_leaks()
    print(f"Update without cluster finding:")
    print(timer.elapsed)

    with count_time() as timer:
        grid.is_leaks()
    print("Update and check leackage")
    print(timer.elapsed)
   
    grid.update()
    with count_time() as timer:
        grid.find_clusters()
    print("Update and find clusters")
    print(timer.elapsed)
