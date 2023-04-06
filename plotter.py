import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from perf_measurer import count_time
from tqdm import tqdm

from grid import Grid

class BasePlotter(tk.Toplevel):
    def __init__(self, parent, size: Tuple[int, int]=(6, 3)) -> None:
        super().__init__(parent)
        self.parent = parent
        
        self.figure = plt.Figure(figsize=size)
        figure_canvas = FigureCanvasTkAgg(self.figure, self)
        NavigationToolbar2Tk(figure_canvas, self)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def update(self) -> None:
        self.figure.clear()
        self.create_axes()
        self.set_labels()
        self.set_data()
        self.figure.canvas.draw_idle()
        
    def create_axes(self) -> None:
        raise NotImplementedError
    
    def set_labels(self) -> None:
        raise NotImplementedError
    
    def set_data(self) -> None:
        raise NotImplementedError

class Sizes_plot(BasePlotter):
    def __init__(self, parent) -> None:
        super().__init__(parent, (6, 6))
        self.grid = Grid(find_all_clusters=False, update_on_init=False, update_on_changes=False)

        #Размеры сетки
        self.sizes = np.arange(10, 40)
        #Вероятность связи
        self.prob_points = np.linspace(0, 1, 20)
        #Количество тестов на каждую сетку
        self.total_n_points = 10**2

        #Количество тестов на кажду вероятность связи
        self.n_tests = np.abs(1/(self.prob_points-0.5))
        self.n_tests = self.n_tests / np.sum(self.n_tests) * self.total_n_points + 1
        self.n_tests = self.n_tests.astype(int)

        self.update()
    
    def calculate_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        data = np.full((*self.prob_points.shape, *self.sizes.shape, 10**4), 
                       float('nan'))

        for y, s in tqdm(enumerate(self.sizes), total=len(self.sizes)):
            self.grid.change_size(s, s)
            for x, p in enumerate(self.prob_points):
                self.grid.change_probability(p)
                for i in range(self.n_tests[x]):
                    self.grid.update()
                    data[x, y, i] = self.grid.is_leaks()
                    
        X, Y = np.meshgrid(self.sizes, self.prob_points)
        Z = np.nanmean(data, axis=2)
        return X, Y, Z
    
    def create_axes(self) -> None:
        self.axes = self.figure.add_subplot(projection='3d')
    
    def set_labels(self) -> None:
        self.axes.set_xlabel("Размер сетки")
        self.axes.set_ylabel("Вероятность связи")
        self.axes.set_zlabel("Шанс Протечки")
    
    def set_data(self) -> None:
        X, Y, Z = self.calculate_data()
        self.axes.plot_surface(X, Y, Z)
    

if __name__ == "__main__":
    root = tk.Tk()
    plot = Sizes_plot(root)

    plot.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()