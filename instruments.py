import tkinter as tk
import tkinter.ttk as ttk

from cluster_info import Cluster_count
from painter import Painter
from settings import *
from widgets import Property_scale


class Instruments_panel(tk.Frame):

    def __init__(self, parent, painter: Painter) -> None:
        super().__init__(parent)
        self.painter = painter
        self.grid = painter.grid
        self.cluster_count = None

        Property_scale(self, 'Grid width', self.update_width, from_=1, to=MAX_GRID, 
                       value=self.painter.grid.width).pack()
        Property_scale(self, 'Grid height', self.update_height, from_=1, to=MAX_GRID,
                       value=self.painter.grid.height).pack()
        
        Property_scale(self, 'Probability', self.update_probability,
                       value=self.painter.grid.prob, step=PROBABILITY_STEP).pack()
        
        Property_scale(self, 'Line lenght', self.update_line_lenght, 
                       to=MAX_LINE_LENGHT, value=self.painter.line_lenght, ).pack()
        Property_scale(self, 'Line width', self.update_line_width, 
                       to=MAX_LINE_WIDTH, value=self.painter.line_width, ).pack()
        Property_scale(self, 'Point diameter', self.update_point_radius, 
                       to=MAX_POINT_RADIUS, value=self.painter.point_diameter).pack()

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
        self.update()
    
    def update_width(self, new_value: int) -> None:
        self.grid.change_size(new_value, None)
        self.update()
    def update_height(self, new_value: int) -> None:
        self.grid.change_size(None, new_value)
        self.update()
        
    def update_probability(self, new_value: int) -> None:
        self.grid.change_probability(new_value)
        self.update()

    def update_line_lenght(self, new_value: int) -> None:
        self.painter.line_lenght = new_value
        self.painter.update(False)
    def update_line_width(self, new_value: int) -> None:
        self.painter.line_width = new_value
        self.painter.update(False)
    def update_point_radius(self, new_value: int) -> None:
        self.painter.point_diameter = new_value
        self.painter.update(False)
    
    def update(self) -> None:
        self.painter.update()
        if self.cluster_count is not None:
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