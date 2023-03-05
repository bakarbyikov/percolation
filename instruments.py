import tkinter as tk
from typing import Callable

from painter import Painter
from settings import *

class Property_scale(tk.Frame):

    def __init__(self, parent, name: str, callback: Callable, 
                 value: int, to: int, from_: int=0,
                 out_float: bool=False):
        super().__init__(parent)
        self.callback = callback
        self.out_float = out_float
        self.scale = tk.Scale(self, from_=from_, to=to,
                              orient=tk.HORIZONTAL,
                              label=name)
        if self.out_float:
            self.scale.config(resolution=PROBABILITY_STEP)
        self.scale.set(value)
        self.scale.bind("<ButtonRelease-1>", self.do_callback)
        self.scale.pack()
    
    def do_callback(self, *_) -> None:
        if self.out_float:
            value = float(self.scale.get())
        else:
            value = int(self.scale.get())
        self.callback(value)

class Instruments(tk.Frame):

    def __init__(self, parent: tk.Frame, painter: Painter) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.painter = painter

        Property_scale(self, 'Grid width', self.update_width,
                       self.painter.grid.width, MAX_GRID).pack()
        Property_scale(self, 'Grid height', self.update_height,
                       self.painter.grid.height, MAX_GRID).pack()
        
        Property_scale(self, 'Probability', self.update_probability,
                       self.painter.grid.prob, 1, out_float=True).pack()
        
        Property_scale(self, 'Line lenght', self.update_line_lenght,
                       self.painter.line_lenght, MAX_LINE_LENGHT).pack()
        Property_scale(self, 'Line width', self.update_line_width,
                       self.painter.line_width, MAX_LINE_WIDTH).pack()
        Property_scale(self, 'Point radius', self.update_point_radius,
                       self.painter.point_radius, MAX_POINT_RADIUS).pack()

        tk.Button(self, text="Update grid", command=self.update_grid).pack(side=tk.BOTTOM)
    
    def update_width(self, new_value: int) -> None:
        self.painter.change_grid_size(new_value, None)
    def update_height(self, new_value: int) -> None:
        self.painter.change_grid_size(None, new_value)
        
    def update_probability(self, new_value: int) -> None:
        self.painter.change_grid_probability(new_value)

    def update_line_lenght(self, new_value: int) -> None:
        self.painter.line_lenght = new_value
        self.painter.update()
    def update_line_width(self, new_value: int) -> None:
        self.painter.line_width = new_value
        self.painter.update()
    def update_point_radius(self, new_value: int) -> None:
        self.painter.point_radius = new_value
        self.painter.update()

    def update_grid(self):
        self.painter.grid.update()
        self.painter.update()

if __name__ == "__main__":
    root = tk.Tk()
    p = Painter(root)
    i = Instruments(root, p)
    p.pack(side=tk.LEFT)
    i.pack(side=tk.LEFT)
    root.mainloop()