import tkinter as tk

from instruments import Instruments_panel
from painter import Painter
from settings import *


class App(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Percolation - Tools")
        self.painter = Painter(self)
        self.instruments = Instruments_panel(self, self.painter)
        self.instruments.adjust_size()
        self.instruments.update()
        self.instruments.pack(pady=20, padx=20)

if __name__ == "__main__":
    App().mainloop()