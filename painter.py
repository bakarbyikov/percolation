import tkinter as tk

import numpy as np
from PIL import Image as im
from PIL import ImageTk as itk

from grid import Grid
from misc import print_elapsed_time
from settings import *


class Painter(tk.Frame):

    def __init__(self, parent: tk.Frame, grid: Grid=None) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.grid = Grid(find_all_clusters=False) if grid is None else grid
        self.create_palette()

        self.line_lenght = LINE_LENGHT
        self.line_width = LINE_WIDTH
        self.padding = PADDING
        self.point_diameter = POINT_DIAMETER
        
        self.canvas = tk.Canvas(self, bg=BACKGROUND_COLOR)
        self.canvas.pack()
        self.update()
        
        self.canvas.bind('<Button-1>', self.on_left_mouse)
        self.canvas.bind('<Button-2>', self.on_middle_mouse)
        self.canvas.bind('<Button-3>', self.on_right_mouse)

    def on_left_mouse(self, *_) -> None:
        self.update_grid()

    def on_middle_mouse(self, *_) -> None:
        self.grid.is_leaks()
        self.create_palette()
        self.update()

    def on_right_mouse(self, *_) -> None:
        self.grid.find_clusters()
        self.create_palette()
        self.update()
    
    def change_grid_probability(self, prob: float) -> None:
        self.grid.change_probability(prob)
        self.update_grid()

    def change_grid_size(self, width: int=None, height: int=None) -> None:
        self.grid.change_size(width, height)
        self.update_grid()
    
    def update_grid(self) -> None:
        with print_elapsed_time("Grid updating"):
            self.grid.update()
        with print_elapsed_time("Canvas updating"):
            self.create_palette()
            self.update()
        
    def update_canvas_size(self) -> None:
        self.offset = self.padding + max(self.line_width, self.point_diameter//2)
        self.width = (self.grid.width-1) * self.line_lenght + self.offset*2
        self.height = (self.grid.height-1) * self.line_lenght + self.offset*2
        self.size = self.width, self.height
        self.canvas.config(width=self.width, height=self.height)
    
    def update(self, size_changed: bool=True) -> None:
        if size_changed:
            self.update_canvas_size()
        self.canvas.delete("all")
        self.draw()
    
    def create_palette(self) -> None:
        n = len(self.grid.clusters_list)
        print(f"{n = }")
        self.palette = np.random.randint(0, 255, (n+1, 3), np.uint8)
        self.palette[-1] = PASSIVE_COLOR
    
    def draw_points(self, surface) -> None:
        cur_circle = np.dstack([circle(self.point_diameter),]*3)
        for i, cluster in enumerate(self.grid.clusters_list):
            color = self.palette[i]
            colored_circle = np.asanyarray(cur_circle[:, :] * color, np.uint8)
            for node in cluster.nodes:
                pos = np.array(node) * self.line_lenght + self.offset - self.point_diameter//2
                blit(surface, colored_circle, pos)

        color = self.palette[-1]
        colored_circle = np.asanyarray(cur_circle[:, :] * color, np.uint8)
        for node in np.argwhere(self.grid.clusters == None):
            pos = node * self.line_lenght + self.offset - self.point_diameter//2
            blit(surface, colored_circle, pos)
    
    def _draw_line(self, surface, pos, is_horisonta):
        if self.grid.clusters[tuple(pos)] is None:
            color = self.palette[-1]
        else:
            color = self.palette[self.grid.clusters[tuple(pos)].name]

        left_top = pos * self.line_lenght + self.offset
        if is_horisonta:
            left_top -= (0, self.line_width//2)
            right_bottom = left_top + (self.line_lenght, self.line_width)
        else:
            left_top -= (self.line_width//2, 0)
            right_bottom = left_top + (self.line_width, self.line_lenght)

        surface[left_top[0]:right_bottom[0], left_top[1]:right_bottom[1], :] = color[:]
    
    def draw_lines(self, surface) -> None:
        for pos in np.argwhere(self.grid.horizontal_links):
            self._draw_line(surface, pos, True)
        for pos in np.argwhere(self.grid.vertical_links):
            self._draw_line(surface, pos, False)

    def compute_image(self):
        black = (0, 0, 0)
        pink = (255, 192, 203)
        surface = np.expand_dims(np.array(black, np.uint8), (0, 1))
        surface = surface.repeat(self.width, axis=0).repeat(self.height, axis=1)
        if self.point_diameter:
            self.draw_points(surface)
        if self.line_width:
            self.draw_lines(surface)
        return surface
    
    def draw(self):
        image = self.compute_image()
        image = image.transpose(1, 0, 2)
        self.ph = itk.PhotoImage(im.fromarray(image))
        self.canvas.create_image(2, 2, anchor=tk.NW, image=self.ph)
        self.canvas.image = self.ph


def circle(diameter: int) -> np.ndarray:
    if diameter == 0:
        raise NotImplementedError(f"Cant compute circle with diameter = 0")
    if diameter == 1:
        return np.array([[1,],], float)
    if diameter == 2:
        return np.array([[1, 1], [1, 1]], float)
    radius = diameter / 2
    mul = 10
    x = np.linspace(-radius, radius, diameter*mul)
    y = np.linspace(-radius, radius, diameter*mul)
    xx, yy = np.meshgrid(x, y)
    zz = (xx**2 + yy**2) <= radius**2
    image = np.zeros((diameter, diameter), float)
    for x, column in enumerate(np.vsplit(zz, diameter)):
        for y, cell in enumerate(np.hsplit(column, diameter)):
            image[x, y] = cell.mean()
    return image

def blit(surface: np.ndarray, image: np.ndarray, pos: np.ndarray) -> None:
    end = pos + image.shape[:2]
    surface[pos[0]:end[0], pos[1]:end[1], :] = image[:, :, :]


if __name__ == "__main__":
    root = tk.Tk()
    p = Painter(root)
    p.pack()
    root.mainloop()
