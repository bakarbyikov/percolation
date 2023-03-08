import tkinter as tk
from tkinter import ttk
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
        self.value = value

        top_part = ttk.Frame(self)
        top_part.pack(fill='x')

        ttk.Label(top_part, text=name+":").pack(side=tk.LEFT)
        vcmd = (self.register(self.validate))
        self.entry = ttk.Entry(top_part, 
                               validate='all', 
                               validatecommand=(vcmd, '%P'))
        self.entry.bind('<Return>', self.do_callback)
        self.entry.bind('<FocusOut>', self.do_callback)
        self.update_label(value)
        self.entry.pack(side=tk.RIGHT)

        bottom_part = ttk.Frame(self)
        bottom_part.pack()
    
        self.scale = ttk.Scale(bottom_part, from_=from_, to=to,
                               value=value,
                               orient=tk.HORIZONTAL,
                               length=SCALE_LENGHT,
                               command=self.update_label)
        self.scale.bind("<ButtonRelease-1>", self.do_callback)
        self.scale.pack()
    
    def update_label(self, new_value) -> None:
        new_value = float(new_value)
        if not self.out_float:
            new_value = round(new_value)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, round(new_value, 2))
        pass
    
    def do_callback(self, *_) -> None:
        if self.out_float:
            value = float(self.entry.get())
        else:
            value = round(float(self.entry.get()))
        if self.value == value:
            return
        self.value = value
        self.callback(value)
    
    def validate(self, P: str) -> bool:
        if len(P) == 0:
            return True
        try:
            float(P)
        except ValueError:
            return False
        else:
            return True
        
class Instruments(tk.Frame):

    def __init__(self, parent: tk.Frame, painter: Painter) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.painter = painter

        Property_scale(self, 'Grid width', self.update_width,
                       self.painter.grid.width, MAX_GRID, from_=1).pack()
        Property_scale(self, 'Grid height', self.update_height,
                       self.painter.grid.height, MAX_GRID, from_=1).pack()
        
        Property_scale(self, 'Probability', self.update_probability,
                       self.painter.grid.prob, 1, out_float=True).pack()
        
        Property_scale(self, 'Line lenght', self.update_line_lenght,
                       self.painter.line_lenght, MAX_LINE_LENGHT).pack()
        Property_scale(self, 'Line width', self.update_line_width,
                       self.painter.line_width, MAX_LINE_WIDTH).pack()
        Property_scale(self, 'Point diameter', self.update_point_radius,
                       self.painter.point_diameter, MAX_POINT_RADIUS).pack()

        tk.Button(self, text="Update grid", command=self.painter.update_grid).pack(side=tk.BOTTOM)
    
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
        self.painter.point_diameter = new_value
        self.painter.update()

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Percolation')
    p = Painter(root)
    i = Instruments(root, p)
    p.pack(side=tk.LEFT)
    i.pack(side=tk.LEFT)
    root.mainloop()