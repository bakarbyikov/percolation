import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from grid import Grid

def do_graph(num: int=20):
    grid = Grid(find_all_clusters=False, update_on_init=False, update_on_changes=False)

    power = 2
    sizes = np.arange(2, 20)
    prob_points = np.linspace(1, 0, num//2, endpoint=False)**power / 2 + 0.5
    prob_points = np.concatenate((prob_points, -np.flip(prob_points)+1))
    prob_points = np.flip(prob_points)
    print(prob_points)
    data = np.full((*prob_points.shape, *sizes.shape, 10**4), float('nan'))
        
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(projection='3d')
    X, Y = np.meshgrid(sizes, prob_points)

    for i in tqdm(range(10**3)):
        for y, s in enumerate(sizes):
            grid.change_size(s, s)
            for x, p in enumerate(prob_points):
                grid.change_probability(p)
                grid.update()
                data[x, y, i] = grid.is_leaks()
    Z = np.nanmean(data, axis=2)
    ax1.clear()
    ax1.plot_surface(X, Y, Z)
    plt.show()

if __name__ == "__main__":
    do_graph()