import gym
from gym import spaces
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class HexChessEnv(gym.Env):
    def __init__(self):
        super(HexChessEnv, self).__init__()
        self.grid_height = 7
        self.grid_width = 10
        self.hex_size = 1
        self.action_space = spaces.Tuple((spaces.Discrete(self.grid_height * self.grid_width),
                                          spaces.Discrete(3)))  # Choose cell and one of three possible moves
        self.observation_space = spaces.Box(low=0, high=2, shape=(self.grid_height, self.grid_width, 1), dtype=np.int8)
        self.reset()

    def step(self, action):
        index, move_option = action
        row, col = index // self.grid_width, index % self.grid_width
        if self.state[row, col, 0] in [1, 2]:  # Check if there's a progressor
            moves = self.possible_moves(row, col, self.state[row, col, 0])
            if move_option < len(moves):
                new_row, new_col = moves[move_option]
                if self.state[new_row, new_col, 0] == 0:  # Move if the target cell is empty
                    self.state[new_row, new_col, 0] = self.state[row, col, 0]
                    self.state[row, col, 0] = 0
                    reward = 1  # Simple reward for a valid move
                else:
                    reward = -1  # Penalty for trying to move to a non-empty cell
            else:
                reward = -1  # Penalty for an invalid move option
        else:
            reward = -1  # Penalty for selecting a cell without a progressor
        done = False  # Game logic to determine if the game is done
        return self.state, reward, done, {}

    def reset(self):
        self.state = np.zeros((self.grid_height, self.grid_width, 1), dtype=np.int8)
        # Initialize positions for White progressors
        for col in range(1, 10, 2):
            self.state[5, col, 0] = 1  # White progressor
        # Initialize positions for Black progressors
        for col in range(1, 10, 2):
            self.state[1, col, 0] = 2  # Black progressor
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

    def possible_moves(self, row, col, piece):
        # Assuming progressors move one step in any of three forward directions
        if piece == 1:  # White moves upwards
            return [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1)]
        elif piece == 2:  # Black moves downwards
            return [(row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
        return []

    def render(self, mode='human'):
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
