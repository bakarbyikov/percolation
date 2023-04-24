from operator import attrgetter
import tkinter as tk
import tkinter.ttk as ttk
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from tqdm import tqdm

from grid import Grid

class BasePlotter(ttk.Frame):
    def __init__(self, parent, size: Tuple[int, int]=(6, 3)) -> None:
        super().__init__(parent)
        self.parent = parent
        
        self.figure = plt.Figure(figsize=size)
        figure_canvas = FigureCanvasTkAgg(self.figure, self)
        NavigationToolbar2Tk(figure_canvas, self)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.data = None
    
    def calculate_data():
        raise NotImplementedError

    def save(self, file):
        np.save(file, self.data)
        
    def open(self, file):
        self.data = np.load(file)
        self.update()
        
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
        self.grid = Grid(find_all_clusters=False, 
                         update_on_init=False, 
                         update_on_changes=False)

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
        self.data = X, Y, Z
    
    def create_axes(self) -> None:
        self.axes = self.figure.add_subplot(projection='3d')
    
    def set_labels(self) -> None:
        self.axes.set_xlabel("Размер сетки")
        self.axes.set_ylabel("Вероятность связи")
        self.axes.set_zlabel("Шанс Протечки")
    
    def set_data(self) -> None:
        X, Y, Z = self.data
        self.axes.plot_surface(X, Y, Z)
    

class Cluster_sizes(BasePlotter):
    def __init__(self, parent) -> None:
        super().__init__(parent, (6, 6))
        self.grid = Grid(find_all_clusters=True, 
                         update_on_init=False, 
                         update_on_changes=False)
    
    def calculate_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        data = np.full(self.grid.width*self.grid.height, int())

        n_grids = 10**5
        count = 0
        for _ in tqdm(range(n_grids)):
            self.grid.update()
            count += len(self.grid.clusters_list)-1
            for c in self.grid.clusters_list[1:]:
                data[c.size] += 1
                    
        X = np.arange(1, data.shape[0])
        Y = data[1:] / count
        self.data = X, Y
    
    def create_axes(self) -> None:
        self.axes = self.figure.add_subplot()
    
    def set_labels(self) -> None:
        self.axes.set_xlabel("Размер кластера")
        self.axes.set_ylabel("Шанс появления")
    
    def set_data(self) -> None:
        X, Y = self.data
        self.axes.plot(X, Y)


class Cluster_sizes_log(Cluster_sizes):
    
    def create_axes(self) -> None:
        self.axes = self.figure.add_subplot()
        self.axes.set_xscale('log')
        self.axes.set_yscale('log')

class AreaPlot(BasePlotter):
    def __init__(self, parent):
        super().__init__(parent, (6, 6))

        self.grid = Grid(40, 40, 
                         find_all_clusters=True, 
                         update_on_init=False, 
                         update_on_changes=True)

        self.eps = np.linspace(0.0, 0.001, 10)
        self.total_n_points = 100
        self.prob_points = np.linspace(0.5-self.eps, 0.5+self.eps, 
                                       self.total_n_points, axis=-1)
        self.get_size = attrgetter('size')
    
    def calculate_data(self) -> None:
        data_max = np.full(self.prob_points.shape, 0)
        data_mean = np.full(self.prob_points.shape, 0.0)

        for index, prob in tqdm(np.ndenumerate(self.prob_points), total=len(self.eps)*self.total_n_points):
            self.grid.change_probability(prob)
            sizes = list(map(self.get_size, self.grid.clusters_list[1:]))
            data_max[index] = max(sizes)
            data_mean[index] = sum(sizes) / len(sizes)

        X = self.eps
        Y = np.mean(data_mean, axis=1)
        self.data = X, Y
    
    def create_axes(self) -> None:
        self.axes = self.figure.add_subplot()
    
    def set_labels(self) -> None:
        self.axes.set_xlabel("Окрестность")
        self.axes.set_ylabel("Средняя площадь кластера")

    def set_data(self) -> None:
        X, Y = self.data
        self.axes.plot(X, Y)
        
class AreaPlot2(BasePlotter):
    def __init__(self, parent):
        super().__init__(parent, (6, 6))
        self.grid = Grid(40, 40, 
                         find_all_clusters=True, 
                         update_on_init=False, 
                         update_on_changes=True)

        self.eps = 0.001
        self.total_n_points = 10**5
        self.prob_points = np.linspace(0.5-self.eps, 0.5+self.eps, 10)
        self.get_size = attrgetter('size')
    
    def calculate_data(self) -> None:
        data_max = np.full((*self.prob_points.shape, self.total_n_points), 0)
        data_mean = np.full((*self.prob_points.shape, self.total_n_points), 0.0)

        for index, prob in tqdm(np.ndenumerate(self.prob_points), total=len(self.prob_points)):
            self.grid.change_probability(prob)
            for i in range(self.total_n_points):
                sizes = list(map(self.get_size, self.grid.clusters_list[1:]))
                data_max[index, i] = max(sizes)
                data_mean[index, i] = sum(sizes) / len(sizes)

        X = self.prob_points
        Y = np.mean(data_mean, axis=-1)
        self.data = X, Y
    
    def create_axes(self) -> None:
        self.axes = self.figure.add_subplot()
    
    def set_labels(self) -> None:
        self.axes.set_xlabel("Вероятность связи")
        self.axes.set_ylabel("Средняя площадь кластера")

    def set_data(self) -> None:
        X, Y = self.data
        self.axes.plot(X, Y)
 
class Average_size(BasePlotter):
    def __init__(self, parent):
        super().__init__(parent, (6, 6))
        self.grid = Grid(40, 40, 
                         find_all_clusters=True, 
                         update_on_init=False, 
                         update_on_changes=False)
        
        self.n_grids = 10**3
        self.prob_points = np.linspace(0, 1, 101)
    
    def distribution_for_prob(self, prob: float):
        self.grid.change_probability(prob)
        distribution = np.zeros(self.grid.width*self.grid.height+1)
        
        count = 0
        for _ in range(self.n_grids):
            self.grid.update()
            count += len(self.grid.clusters_list)-1
            for c in self.grid.clusters_list[1:]:
                distribution[c.size] += 1
        distribution /= self.grid.width*self.grid.height * self.n_grids
        return distribution
    
    def calculate_data(self) -> None:
        sizes_squere = np.arange(self.grid.width*self.grid.height+1)**2
        data = np.empty(self.prob_points.shape)

        for i, prob in enumerate(tqdm(self.prob_points)):
            distribution = self.distribution_for_prob(prob)
            data[i] = np.sum(sizes_squere * distribution)
                    
        X = self.prob_points
        Y = data
        self.data = X, Y
    
    def create_axes(self) -> None:
        self.axes = self.figure.add_subplot()
    
    def set_labels(self) -> None:
        self.axes.set_xlabel("Вероятность связи")
        self.axes.set_ylabel("Средний размер кластера")

    def set_data(self) -> None:
        X, Y = self.data
        self.axes.plot(X, Y)


if __name__ == "__main__":
    root = tk.Tk()
    plot = Average_size(root)
    plot.pack(fill=tk.BOTH, expand=True)
    plot.calculate_data()
    plot.save("Average_size_plot")
    plot.update()

    root.mainloop()