import tkinter as tk

from instruments import Instruments
from painter import Painter
from settings import *


class App(tk.Frame):

    def __init__(self, parent, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        painter_window = tk.Toplevel(self)
        painter_window.protocol("WM_DELETE_WINDOW", root.destroy)
        self.painter = Painter(painter_window)
        self.painter.pack()

        self.instruments = Instruments(self, self.painter)
        self.instruments.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Percolation")
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()