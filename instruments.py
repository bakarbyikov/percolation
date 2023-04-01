from math import ceil
import tkinter as tk
import tkinter.ttk as ttk

from cluster_info import Cluster_count
from painter import Painter
from settings import *
from widgets import Property_scale


class Instruments_panel(tk.Frame):

    def __init__(self, parent, painter: Painter) -> None:
        super().__init__(parent)
        self.parent = parent
        self.painter = painter
        self.grid = painter.grid
        self.cluster_count = None

        self.line_width = LINE_WIDTH_REL
        self.gap_size = GAP_SIZE

        Property_scale(self, 'Grid width', self.update_width, from_=1, to=MAX_GRID, 
                       value=self.painter.grid.width).pack()
        Property_scale(self, 'Grid height', self.update_height, from_=1, to=MAX_GRID,
                       value=self.painter.grid.height).pack()
        
        Property_scale(self, 'Probability', self.update_probability,
                       value=self.painter.grid.prob, step=PROBABILITY_STEP).pack()
        
        Property_scale(self, 'Line width', self.update_line_width,
                       value=self.line_width, step=0.1).pack()
        Property_scale(self, 'Point size', self.update_gap_size,
                       value=self.gap_size, step=0.1).pack()

        buttons = ttk.Frame(self)
        buttons.pack(side=tk.BOTTOM)
        ttk.Button(buttons, text="Update grid", 
                  command=self.update_grid).pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons, text="Clusters size", 
                  command=self.plot_clusters).pack(side=tk.LEFT, padx=10)
    
    def plot_clusters(self) -> None:
        if self.cluster_count is None:
            self.cluster_count = Cluster_count(self, self.grid)
        else:
            self.cluster_count.destroy()
            self.cluster_count = Cluster_count(self, self.grid)
    
    def update_grid(self) -> None:
        self.grid.update()
        self.adjust_size()
        self.update()
    
    def update_line_width(self, value: int|float) -> None:
        self.line_width = value
        self.update_line()
        self.update(False)
    def update_gap_size(self, value: int|float) -> None:
        self.gap_size = value
        self.update_line()
        self.update(False)
    
    def update_line(self) -> None:
        self.painter.point_diameter = ceil(self.painter.line_lenght*self.gap_size)
        self.painter.line_width = round(self.painter.point_diameter*self.line_width)

    def adjust_size(self) -> None:
        screen_width = self.painter.winfo_width()-self.painter.padding*2
        screen_height = self.painter.winfo_height()-self.painter.padding*2
        self.painter.line_lenght = min(max(int(screen_width / self.grid.width), 1),
                                       max(int(screen_height / self.grid.height), 1))
        self.update_line()
    
    def update_width(self, new_value: int) -> None:
        self.grid.change_size(new_value, None)
        self.adjust_size()
        self.update()
    def update_height(self, new_value: int) -> None:
        self.grid.change_size(None, new_value)
        self.adjust_size()
        self.update()
        
    def update_probability(self, new_value: int) -> None:
        self.grid.change_probability(new_value)
        self.update()
    
    def update(self, grid_changed: bool=True) -> None:
        self.painter.update(grid_changed)
        if self.cluster_count is not None and grid_changed:
            self.cluster_count.update()

if __name__ == "__main__":
    root = tk.Tk()
    p = Painter(root)
    p.destroy()
    p.update = lambda *args: None
    p.grid.update = lambda *args: None
    i = Instruments_panel(root, p)
    i.pack()
    root.mainloop()