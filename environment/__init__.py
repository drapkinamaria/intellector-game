import gym
from gym import spaces
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class HexChessEnv(gym.Env):
    def __init__(self, grid_height=7, grid_width=10, hex_size=1):
        super(HexChessEnv, self).__init__()
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.hex_size = hex_size
        self.action_space = spaces.Discrete(grid_height * grid_width)
        self.observation_space = spaces.Box(low=0, high=2,
                                            shape=(grid_height, grid_width, 1),
                                            dtype=np.int32)

        self.state = None
        self.reset()

    def step(self, action):
        self.state = self._next_state(self.state, action)
        reward = self._calculate_reward(self.state, action)
        done = self._check_done(self.state)
        info = {}
        return self.state, reward, done, info

    def reset(self):
        self.state = np.zeros((self.grid_height, self.grid_width, 1), dtype=np.int32)
        return self.state

    def choose_color(self, row, col):
        color_peru = [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9),
                     (2, 2), (2, 4), (2, 6), (2, 8),
                     (3, 1), (3, 3), (3, 5), (3, 7), (3, 9),
                     (5, 2), (5, 4), (5, 6), (5, 8),
                     (6, 1), (6, 3), (6, 5), (6, 7), (6, 9)
                     ]
        if (row, col) in color_peru:
            return True
        else:
            return

    def render(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

        dx = 3 / 2 * self.hex_size
        dy = np.sqrt(3) * self.hex_size
        exclude_indices = [(0, 2), (0, 4), (0, 6), (0, 8)]

        for col in range(1, self.grid_width):
            rows = self.grid_height
            for row in range(rows):
                if (row, col) in exclude_indices:
                    continue
                x = dx * col
                y = dy * row + (col % 2) * dy / 2
                if self.choose_color(row, col):
                    color = 'peru'
                else:
                    color = 'moccasin'
                self.draw_hexagon(ax, (x, y), self.hex_size, color)
                ax.text(x, y, f'{row},{col}', ha='center', va='center', color='black', fontsize=10)

        ax.set_xlim([0, dx * self.grid_width])
        ax.set_ylim([0, dy * (self.grid_height + 2)])

        ax.invert_yaxis()
        plt.show()

    def draw_hexagon(self, ax, center, size, color):
        hexagon = patches.RegularPolygon(center, numVertices=6, radius=size,
                                         orientation=np.radians(30),
                                         facecolor=color, edgecolor='sienna')
        ax.add_patch(hexagon)

    def _next_state(self, state, action):
        return state

    def _calculate_reward(self, state, action):
        return 0

    def _check_done(self, state):
        return False


env = HexChessEnv()
env.render()
