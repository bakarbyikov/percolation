import tkinter as tk
from tkinter import ttk
from typing import Callable

from settings import *


class Property_scale(tk.Frame):

    def __init__(self, parent, name: str, callback: Callable, 
                 value: int, to: int, from_: int=0,
                 step: float=1, out_float: bool=False):
        super().__init__(parent)
        self.callback = callback
        self.out_float = out_float
        self.value = value

        top_part = ttk.Frame(self)
        top_part.pack(fill='x', pady=(5, 0), padx=5)

        ttk.Label(top_part, text=name+":").pack(side=tk.LEFT)
        vcmd = (self.register(self.validate))
        self.entry = ttk.Spinbox(top_part, 
                                 from_=from_, to=to,
                                 increment=step,
                                 command=self.do_callback,
                                 validate='all',
                                 validatecommand=(vcmd, '%P'))
        self.entry.bind('<Return>', self.do_callback)
        self.entry.bind('<FocusOut>', self.do_callback)
        self.update_label(value)
        self.entry.pack(side=tk.RIGHT)

        bottom_part = ttk.Frame(self)
        bottom_part.pack(pady=(0, 15))
    
        self.scale = tk.Scale(bottom_part, from_=from_, to=to,
                              showvalue=False,
                              resolution=step,
                              orient=tk.HORIZONTAL,
                              length=SCALE_LENGHT,
                              command=self.update_label)
        self.scale.set(value)
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
        self.scale.set(float(self.entry.get()))
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