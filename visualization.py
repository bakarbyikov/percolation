import tkinter as tk
import tkinter.ttk as ttk
from painter import Painter
from instruments import Instruments_panel


class Visualization(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        painter = Painter(self)
        tools = Instruments_panel(self, painter)

        painter.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        tools.pack(fill=tk.Y, side=tk.LEFT)