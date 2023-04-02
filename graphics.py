from math import ceil

import numpy as np
from PIL import Image as im

from grid import Grid
from settings import *


class Drawer:

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.create_palette()

        self.line_lenght = None
        self.line_width = None
        self.point_diameter = None
        
        self.width, self.height = None, None
        self.size = self.width, self.height

        self.background = BACKGROUND_COLOR
    
    def set_properties(self, line_lenght, line_width, point_diameter) -> None:
        self.line_lenght = line_lenght
        self.line_width = line_width
        self.point_diameter = point_diameter
        
    def create_palette(self) -> None:
        n_colors = len(self.grid.clusters_list)
        self.palette = np.random.randint(0, 255, (n_colors+1, 3), np.uint8)
        self.palette[0] = PASSIVE_COLOR
    
    def compute_image(self) -> im.Image:
        self.calculate_size()
        self.compute_colors()
        surface = np.tile(self.background, (self.width, self.height, 1)).astype(np.uint8)
        if self.point_diameter:
            self.draw_points(surface)
        if self.line_width:
            self.draw_lines(surface, True)
            self.draw_lines(surface, False)
        surface = surface.transpose(1, 0, 2)
        image = im.fromarray(surface)
        return image
    
    def calculate_size(self) -> tuple[int, int]:
        self.offset = max(self.line_width, self.point_diameter)
        self.offset_lt = self.offset // 2
        self.offset_rb = self.offset - self.offset_lt

        if self.offset > self.line_lenght:
            raise NotImplementedError(f"Cant draw image with overlaps!")

        self.width = (self.grid.width-1) * self.line_lenght + self.offset
        self.height = (self.grid.height-1) * self.line_lenght + self.offset
        self.size = self.width, self.height

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

        
if __name__ == '__main__':
    d = Drawer(Grid())
    d.compute_image().show()