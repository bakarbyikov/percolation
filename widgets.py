import tkinter as tk
from tkinter import ttk
from typing import Callable

from settings import *


class Property_scale(tk.Frame):

    def __init__(self, parent, name: str, callback: Callable, *,
                 from_: int|float=0, to: int|float=1, 
                 value: int|float=0, step: int|float=1):
        super().__init__(parent)
        self.callback = callback
        self.value = value
        self.out_float = not (isinstance(step, int) or step.is_integer())
        if self.out_float:
            self.n_digits = min(len(str(step).split('.')[1]), 6)
            self.mul = 10**self.n_digits
        else:
            self.n_digits = 0
            self.mul = 1

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
    
        self.scale = ttk.Scale(bottom_part, from_=from_*self.mul, to=to*self.mul, 
                               orient=tk.HORIZONTAL, length=SCALE_LENGHT, 
                               command=self.update_label)
        self.scale.set(value*self.mul)
        self.scale.bind("<ButtonRelease-1>", self.do_callback)
        self.scale.pack()
    
    def update_label(self, new_value: str) -> None:
        new_value = int(float(new_value))
        if self.out_float:
            new_value /= self.mul
        self.entry.delete(0, tk.END)
        self.entry.insert(0, round(new_value, self.n_digits))
        pass
    
    def do_callback(self, *_) -> None:
        if self.out_float:
            value = float(self.entry.get())
        else:
            value = round(float(self.entry.get()))
        self.scale.set(float(self.entry.get())*self.mul)
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