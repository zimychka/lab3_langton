import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap


class LangtonAnt:
    def __init__(self, grid_size=100, steps=30000):
        self.grid_size = grid_size
        self.steps = steps
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        self.ant_pos = [grid_size // 2, grid_size // 2]
        self.ant_dir = 0  # 0 - вверх, 1 - направо, 2 - вниз, 3 - влево
        self.step_count = 0
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def move_ant(self):
        x, y = self.ant_pos

        if self.grid[x, y] == 0:
            self.ant_dir = (self.ant_dir + 1) % 4
            self.grid[x, y] = 1

        else:
            self.ant_dir = (self.ant_dir - 1) % 4
            self.grid[x, y] = 0

        dx, dy = self.directions[self.ant_dir]
        self.ant_pos[0] = (x + dx) % self.grid_size
        self.ant_pos[1] = (y + dy) % self.grid_size

        self.step_count += 1

    def simulate(self, num_steps=None):
        if num_steps is None:
            num_steps = self.steps

        for _ in range(num_steps):
            self.move_ant()

    def get_grid_with_ant(self):
        grid_copy = self.grid.copy()
        x, y = self.ant_pos

        grid_copy[x, y] = 2
        return grid_copy


def create_animation():
    grid_size = 100
    total_steps = 30000
    animation_steps = 2000
    steps_per_frame = total_steps // animation_steps

    ant = LangtonAnt(grid_size=grid_size, steps=total_steps)

    fig, ax = plt.subplots(figsize=(10, 10))
    cmap = ListedColormap(['white', 'black', 'red'])

    im = ax.imshow(ant.get_grid_with_ant(), cmap=cmap, vmin=0, vmax=2)
    ax.set_title(f'Муравей Лэнгтона - Шаг: 0')
    ax.set_xticks([])
    ax.set_yticks([])

    def update(frame):
        ant.simulate(steps_per_frame)
        im.set_array(ant.get_grid_with_ant())
        progress = (ant.step_count / total_steps) * 100
        ax.set_title(
            f'Муравей Лэнгтона - Шаг: {ant.step_count} ({progress:.1f}%)')

        return [im, ax.title]

    anim = FuncAnimation(fig, update, frames=animation_steps,
                         interval=50, blit=False, repeat=False)

    plt.tight_layout()
    plt.show()

    return anim


def create_static_plot():
    grid_size = 150
    total_steps = 30000

    ant = LangtonAnt(grid_size=grid_size, steps=total_steps)
    ant.simulate()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

    im1 = ax1.imshow(ant.grid, cmap='binary', interpolation='nearest')
    ax1.set_title(f'Сетка после {total_steps} шагов ')
    ax1.set_xticks([])
    ax1.set_yticks([])

    cmap_with_ant = ListedColormap(['white', 'black', 'red'])
    im2 = ax2.imshow(ant.get_grid_with_ant(), cmap=cmap_with_ant,
                     vmin=0, vmax=2, interpolation='nearest')
    ax2.set_title(f'Сетка с муравьев после {total_steps} шагов')
    ax2.set_xticks([])
    ax2.set_yticks([])

    from matplotlib.patches import Patch
    legend_element = [
        Patch(facecolor='white', edgecolor='black', label='Белая клетка'),
        Patch(facecolor='black', edgecolor='black', label='Черная клетка'),
        Patch(facecolor='red', edgecolor='red', label='Муравей')
    ]
    ax2.legend(handles=legend_element, loc='upper right')

    plt.tight_layout()
    plt.show()


def main_func():
    choice = int(input('anim or the last static plot (1 or 2)?: '))
    if choice == 1:
        create_animation()
    elif choice == 2:
        create_static_plot()
    else:
        print('wrong choice, so the anim is creating...')
        create_animation()


main_func()
