import tkinter as tk
from tkinter import ttk
from typing import Callable

from settings import *


class Property_scale(tk.Frame):

    def __init__(self, parent, name: str, command: Callable, *,
                 from_: int|float=0, to: int|float=1, 
                 value: int|float=0, step: int|float=1):
        super().__init__(parent)
        self.callback = command
        self.value = value
        
        top_part = ttk.Frame(self)
        top_part.pack(fill='x', pady=(5, 0), padx=5)
        ttk.Label(top_part, text=name+":").pack(side=tk.LEFT)
        self.entry = Spinbox(top_part,
                             from_=from_, to=to,
                             step=step, value=value,
                             command=self.on_entry_update)
        self.entry.pack(side=tk.RIGHT)

        bottom_part = ttk.Frame(self)
        bottom_part.pack(pady=(0, 15))
        self.scale = Scale(bottom_part, 
                           from_=from_, to=to,
                           step=step, value=value,
                           orient=tk.HORIZONTAL, length=SCALE_LENGHT, 
                           command=self.on_scale_update)
        self.scale.bind("<ButtonRelease-1>", self.do_callback)
        self.scale.pack()
    
    def on_entry_update(self, value: int|float) -> None:
        self.scale.set(value)
        self.do_callback()
    
    def on_scale_update(self, value: int|float) -> None:
        self.entry.set(value)
    
    def do_callback(self, *_) -> None:
        value = self.entry.get()
        if self.value == value:
            return
        self.value = value
        self.callback(value)
    

class Spinbox(ttk.Spinbox):
    
    def __init__(self, parent, *, from_: int|float=0, to: int|float=1,
                 step: int|float=1, value: int|float=0,
                 command: Callable[[int|float], None], **kwargs) -> None:
        self.callback = command
        self.ignore_callback = False
        self.out_float = not (isinstance(step, int) or step.is_integer())

        super().__init__(parent, from_=from_, to=to,
                         command=self.command, increment=step, **kwargs)
        
        vcmd = self.register(self.validate)
        self.configure(validate='all', validatecommand=(vcmd, '%P'))
        
        self.bind('<Return>', self.command)
        self.bind('<FocusOut>', self.command)
        self.set(value)
        
    def _process_value(self, value: str) -> int|float:
        if self.out_float:
            return float(value)
        return round(float(value))
    
    def command(self, *_) -> None:
        if self.ignore_callback:
            return
        value = self.get()
        self.callback(value)
    
    def set(self, value: int|float) -> None:
        self.ignore_callback = True
        self.delete(0, tk.END)
        self.insert(0, value)
        self.ignore_callback = False

    def get(self) -> int|float:
        return self._process_value(super().get())
    
    def validate(self, P: str) -> bool:
        if len(P) == 0:
            return True
        try:
            float(P)
        except ValueError:
            return False
        else:
            return True


class Scale(ttk.Scale):

    def __init__(self, parent, *, from_: int|float=0, to: int|float=1,
                 step: int|float=1, value: int|float=0,
                 command: Callable[[int|float], None], **kwargs) -> None:
        self.callback = command
        self.ignore_callback = False
        self.out_float = not (isinstance(step, int) or step.is_integer())
        if self.out_float:
            self.n_digits = min(len(str(step).split('.')[1]), 6)
            self.mul = 10**self.n_digits
            from_ *= self.mul
            to *= self.mul
        else:
            self.n_digits = 0
            self.mul = 1

        super().__init__(parent, from_=from_, to=to, command=self.command, **kwargs)
        self.set(value)
    
    def _process_value(self, value: float) -> int|float:
        value = round(value)
        if self.out_float:
            value /= self.mul
        return value
    
    def command(self, value: str) -> None:
        if self.ignore_callback:
            return
        value = self._process_value(float(value))
        self.callback(value)
    
    def set(self, value: int|float) -> None:
        self.ignore_callback = True
        super().set(value*self.mul)
        self.ignore_callback = False
    
    def get(self) -> int|float:
        return self._process_value(super().get())
        

if __name__ == "__main__":
    from random import random
    root = tk.Tk()
    entry = Property_scale(root, "hello", step=1, to=100, command=lambda x: print(f"Now value: {x}"))
    entry.pack(padx=40, pady=(40, 5))
    b = ttk.Button(root)
    b.pack(padx=40, pady=(5, 40))
    b.configure(command=lambda: entry.set(random()))
    root.mainloop()