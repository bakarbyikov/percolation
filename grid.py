from itertools import product
from secrets import token_hex
from typing import Iterable, List, Tuple

import numpy as np

from settings import *


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
    def __init__(self, x: int, y: int, cluster: Cluster) -> None:
        self.coords = (x, y)
        self.cluster = cluster
        self.color = 'black' if cluster is None else self.cluster.color
        
class Grid:

    def __init__(self, width: int=WIDTH, height: int=HEIGHT) -> None:
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


if __name__ == '__main__':
    w, h = 10, 5
    grid = Grid(w, h)
    grid.update()
    print(f"{grid.is_leaks() = }")
    grid.find_clusters()
    table = [[0]*w for _ in range(h)]
    for point in grid.nodes_list():
        x, y = point.coords
        table[y][x] = grid.clusters[x, y].name
    
    for row in table:
        print('\t'.join(map(str, row)))

