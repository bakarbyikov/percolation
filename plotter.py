import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from grid import Grid

def do_graph():
    grid = Grid(find_all_clusters=False, update_on_init=False, update_on_changes=False)

    #Размеры сетки
    sizes = np.arange(10, 40)
    #Вероятность связи
    prob_points = np.linspace(0, 1, 20)
    #Количество тестов на каждую сетку
    total_n_points = 10**4

    #Количество тестов на кажду вероятность связи
    n_tests = np.abs(1/(prob_points-0.5))
    n_tests = n_tests / np.sum(n_tests) * total_n_points + 1
    n_tests = n_tests.astype(int)

    data = np.full((*prob_points.shape, *sizes.shape, 10**4), float('nan'))

    for y, s in tqdm(enumerate(sizes), total=len(sizes)):
        grid.change_size(s, s)
        for x, p in enumerate(prob_points):
            grid.change_probability(p)
            for i in range(n_tests[x]):
                grid.update()
                data[x, y, i] = grid.is_leaks()
                
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(projection='3d')
    ax1.set_xlabel("Размер сетки")
    ax1.set_ylabel("Вероятность связи")
    ax1.set_zlabel("Шинс Протечки")
    X, Y = np.meshgrid(sizes, prob_points)
    Z = np.nanmean(data, axis=2)
    ax1.plot_surface(X, Y, Z)
    plt.show()

if __name__ == "__main__":
    do_graph()