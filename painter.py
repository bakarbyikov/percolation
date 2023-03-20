import tkinter as tk
from math import ceil
from typing import Tuple

import numpy as np
from PIL import Image as im
from PIL import ImageTk as itk

from cluster_info import Cluster_info
from grid import Grid
from misc import color_from_rgb
from settings import *


class Painter(tk.Toplevel):

    def __init__(self, parent, grid: Grid=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title("Percolation - Grid")
        self.protocol("WM_DELETE_WINDOW", self.parent.destroy)
        self.grid = Grid() if grid is None else grid
        self.create_palette()

        self.line_lenght = LINE_LENGHT
        self.line_width = LINE_WIDTH
        self.padding = PADDING
        self.point_diameter = POINT_DIAMETER
        
        self.canvas = tk.Canvas(self, bg=color_from_rgb(BACKGROUND_COLOR))
        self.canvas.pack()
        self.update()
        self.cluster_info = None
        
        self.canvas.bind('<Button-1>', self.on_left_mouse)
        self.canvas.bind('<Button-2>', self.on_middle_mouse)
        self.canvas.bind('<Button-3>', self.on_right_mouse)

    def on_left_mouse(self, event) -> None:
        self.show_cluster_info((event.x, event.y))

    def on_middle_mouse(self, *_) -> None:
        self.grid.is_leaks()
        self.create_palette()
        self.update()

    def on_right_mouse(self, *_) -> None:
        self.grid.find_clusters()
        self.create_palette()
        self.update()

    def show_cluster_info(self, widget_coord: Tuple[int, int]) -> None:
        x, y = self.widget_coords_to_grid(widget_coord)
        cluster = self.grid.get_cluster_on(x, y)
        if self.cluster_info is not None:
            self.cluster_info.destroy()
        self.cluster_info = Cluster_info(self, cluster)
    
    def widget_coords_to_grid(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        pos = np.array(coord)
        pos -= self.offset_lt
        pos -= self.padding
        pos = np.around(pos / self.line_lenght).astype(int)
        pos = np.maximum(pos, [0, 0])
        pos = np.minimum(pos, [self.grid.width-1, self.grid.height-1])
        return tuple(pos)
        
    def update_canvas_size(self) -> None:
        self.offset = max(self.line_width, self.point_diameter)
        self.offset_lt = self.offset // 2
        self.offset_rb = self.offset - self.offset_lt

        if self.offset > self.line_lenght:
            raise NotImplementedError(f"Cant draw image with overlaps!")

        self.width = (self.grid.width-1) * self.line_lenght + self.offset
        self.height = (self.grid.height-1) * self.line_lenght + self.offset
        self.size = self.width, self.height
        self.canvas.config(width=self.width+self.padding*2, height=self.height+self.padding*2)
    
    def update(self, grid_changed: bool=True) -> None:
        self.update_canvas_size()
        if grid_changed:
            self.create_palette()
        self.canvas.delete("all")
        self.draw()
    
    def create_palette(self) -> None:
        n = len(self.grid.clusters_list)
        self.palette = np.random.randint(0, 255, (n+1, 3), np.uint8)
        self.palette[0] = PASSIVE_COLOR
    
    def compute_colors(self) -> None:
        color_surface = np.tile(self.grid.clusters, (3, 1, 1)).transpose(1, 2, 0)
        for z in range(3):
            color_surface[..., z] = self.palette[color_surface[..., z], z]
        color_surface = color_surface.repeat(self.line_lenght, axis=0)\
            .repeat(self.line_lenght, axis=1)
        
        gap = self.line_lenght - self.offset
        if gap:
            color_surface = color_surface[:-gap, :-gap]
        
        self.color_surface = color_surface
    
    def draw_points(self, surface) -> None:
        circle = compute_circle(self.point_diameter)
        gap = self.line_lenght - self.point_diameter
        padded_circle = np.pad(circle, ((0, gap), (0, gap)))
        circle_mask = np.tile(padded_circle, (3, self.grid.width, self.grid.height))\
            .transpose(1, 2, 0)
        if gap:
            circle_mask = circle_mask[:-gap, :-gap]

        offset_lt = self.offset_lt - self.point_diameter // 2
        offset_rb = self.offset_rb - ceil(self.point_diameter / 2)
        padded_mask = np.pad(circle_mask, ((offset_lt, offset_rb),
                                           (offset_lt, offset_rb),
                                           (0, 0)))

        blit(surface, self.color_surface, padded_mask)
    
    def draw_lines(self, surface, is_horisontal: bool) -> None:
        if is_horisontal:
            target = self.grid.horizontal_links
        else:
            target = self.grid.vertical_links.T
        gap = self.line_lenght - self.line_width
        lines = target.repeat(self.line_lenght, axis=0)\
            .repeat(self.line_lenght, axis=1)[:-self.line_lenght]
        line_mask = np.concatenate((np.ones((lines.shape[0], self.line_width)),
                                    np.zeros((lines.shape[0], gap))), axis=1)
        lines_mask = np.tile(line_mask, (1, target.shape[1]))
        masked_lines = lines * lines_mask
        if gap:
            masked_lines = masked_lines[:, :-gap]

        offset_t = self.offset_lt - self.line_width // 2
        offset_b = self.offset_rb - ceil(self.line_width / 2)
        padded_mask = np.pad(masked_lines, ((self.offset_lt, self.offset_rb),
                                            (offset_t, offset_b)))
        if not is_horisontal:
            padded_mask = padded_mask.T

        epanded_mask = np.tile(padded_mask, (3, 1, 1)).transpose(1, 2, 0)
        
        blit(surface, self.color_surface, epanded_mask)


    def compute_image(self):
        self.compute_colors()
        surface = np.tile(BACKGROUND_COLOR, (self.width, self.height, 1)).astype(np.uint8)
        if self.point_diameter:
            self.draw_points(surface)
        if self.line_width:
            self.draw_lines(surface, True)
            self.draw_lines(surface, False)
        return surface
    
    def draw(self):
        image = self.compute_image()
        image = image.transpose(1, 0, 2)
        self.ph = itk.PhotoImage(im.fromarray(image))
        self.canvas.create_image(self.padding+2, self.padding+2, 
                                 anchor=tk.NW, image=self.ph)
        self.canvas.image = self.ph


def compute_circle(diameter: int) -> np.ndarray:
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

def blit(surface: np.ndarray, image: np.ndarray, mask: np.ndarray) -> None:
    surface[...] = surface * (1-mask)
    surface[...] = surface + image * mask


if __name__ == "__main__":
    root = tk.Tk()
    p = Painter(root)
    p.pack()
    root.mainloop()
