import tkinter as tk
from math import ceil
from typing import Tuple

import numpy as np
from PIL import ImageTk as itk

from cluster_info import Cluster_info
from graphics import Drawer
from grid import Grid
from misc import color_from_rgb
from settings import *


class Painter(tk.Toplevel):

    def __init__(self, parent, grid: Grid=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.geometry("x".join(map(str, WINDOW_ZISE)))
        self.title("Percolation - Grid")
        self.grid = Grid() if grid is None else grid
        self.drawer = Drawer(self.grid)

        self.padding = PADDING
        self.line_size = LINE_SIZE
        self.gap_size = GAP_SIZE
        self.size = None, None
        
        self.canvas = tk.Canvas(self, bg=color_from_rgb(BACKGROUND_COLOR), 
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.cluster_info = None
        self.point = None
        
        self.canvas.bind('<Button-1>', self.on_left_mouse)
        self.canvas.bind('<Button-2>', self.on_middle_mouse)
        self.canvas.bind('<Button-3>', self.on_right_mouse)
        self.resizing = None
        self.bind('<Configure>', self.on_configure)
    
    def on_configure(self, event) -> None:
        new_size = event.width, event.height
        if new_size == self.size:
            return
        self.size = new_size
        if self.resizing is not None:
            self.after_cancel(self.resizing)
        self.resizing = self.after(100, self.on_resize)
    
    def on_resize(self) -> None:
        self.resizing = None
        self.update(grid_changed=False)

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
        x, y = self.widget_pos_to_grid(widget_coord)
        cluster = self.grid.get_cluster_on(x, y)
        center = self.grid_pos_to_widget(cluster.center_of_mass)
        r = cluster.radius * self.drawer.point_diameter
        x0, y0 = center - r
        x1, y1 = center + r
        if self.point is not None:
            self.canvas.delete(self.point)
        self.point = self.canvas.create_oval(x0, y0, x1, y1, fill="red")
        self.canvas.update()
        if self.cluster_info is not None:
            self.cluster_info.destroy()
        self.cluster_info = Cluster_info(self, cluster)
        
    def grid_pos_to_widget(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        pos = np.array(coord)
        pos *= self.drawer.line_lenght
        pos += [self.canvas.winfo_width()//2, self.canvas.winfo_height()//2]
        pos -= [self.drawer.width//2, self.drawer.height//2]
        pos += self.drawer.offset_lt
        return pos
    
    def widget_pos_to_grid(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        pos = np.array(coord)
        pos -= [self.canvas.winfo_width()//2, self.canvas.winfo_height()//2]
        pos += [self.drawer.width//2, self.drawer.height//2]
        pos = np.around(pos / self.drawer.line_lenght).astype(int)
        pos = np.maximum(pos, [0, 0])
        pos = np.minimum(pos, [self.grid.width-1, self.grid.height-1])
        return tuple(pos)
    
    def update_line(self) -> None:
        image_width = self.winfo_width() - self.padding*2
        image_height = self.winfo_height() - self.padding*2
        line_lenght = max(1, min(int(image_width / (self.grid.width-1)), 
                                 int(image_height / (self.grid.height-1))))
        
        point_diameter = ceil(line_lenght * self.gap_size)
        line_width = round(point_diameter * self.line_size)
        self.drawer.set_properties(line_lenght,
                                   line_width,
                                   point_diameter)

    def on_grid_change(self) -> None:
        self.update()
    def on_propery_change(self) -> None:
        self.update(grid_changed=False)
    def update(self, property_changed: bool=True, grid_changed: bool=True) -> None:
        if grid_changed:
            self.drawer.create_palette()
        if property_changed:
            self.update_line()
        self.canvas.delete("all")
        self.draw()
    
    def draw(self):
        image = self.drawer.compute_image()
        self.ph = itk.PhotoImage(image)
        self.canvas.create_image(self.canvas.winfo_width()//2, 
                                 self.canvas.winfo_height()//2, 
                                 anchor=tk.CENTER, image=self.ph)
        self.canvas.image = self.ph

if __name__ == "__main__":
    root = tk.Tk()
    p = Painter(root)
    b1 = tk.Button(root, text='grid', command=p.on_grid_change)
    b2 = tk.Button(root, text='prop', command=p.on_propery_change)
    b1.pack(); b2.pack()
    root.mainloop()
