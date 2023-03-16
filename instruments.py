import tkinter as tk

from painter import Painter
from plotter import Cluster_count
from settings import *
from widgets import Property_scale


class Instruments_panel(tk.Frame):

    def __init__(self, parent, painter: Painter) -> None:
        super().__init__(parent)
        self.painter = painter
        self.grid = painter.grid
        self.cluster_count = None

        Property_scale(self, 'Grid width', self.update_width,
                       self.painter.grid.width, MAX_GRID, from_=1).pack()
        Property_scale(self, 'Grid height', self.update_height,
                       self.painter.grid.height, MAX_GRID, from_=1).pack()
        
        Property_scale(self, 'Probability', self.update_probability,
                       self.painter.grid.prob, 1, step=PROBABILITY_STEP, 
                       out_float=True).pack()
        
        Property_scale(self, 'Line lenght', self.update_line_lenght,
                       self.painter.line_lenght, MAX_LINE_LENGHT).pack()
        Property_scale(self, 'Line width', self.update_line_width,
                       self.painter.line_width, MAX_LINE_WIDTH).pack()
        Property_scale(self, 'Point diameter', self.update_point_radius,
                       self.painter.point_diameter, MAX_POINT_RADIUS).pack()

        buttons = tk.Frame(self)
        buttons.pack(side=tk.BOTTOM)
        tk.Button(buttons, text="Update grid", 
                  command=self.update_grid).pack(side=tk.LEFT, padx=10)
        tk.Button(buttons, text="Clusters size", 
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
    i = Instruments_panel(root, p)
    i.pack()
    root.mainloop()