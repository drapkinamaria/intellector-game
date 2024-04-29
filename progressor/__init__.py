class Progressor:
    def __init__(self, position, color):
        self.position = position
        self.color = color  # 'white' or 'black'

    def possible_moves(self, grid_height, grid_width):
        moves = []
        row, col = self.position
        if self.color == 'white':
            if col > 0:
                moves.append((row, col - 1))  # Move left
            if col < grid_width - 1:
                moves.append((row, col + 1))  # Move right
            if row > 0:
                moves.append((row - 1, col))  # Move up
        elif self.color == 'black':
            if col > 0:
                moves.append((row, col - 1))  # Move left
            if col < grid_width - 1:
                moves.append((row, col + 1))  # Move right
            if row < grid_height - 1:
                moves.append((row + 1, col))  # Move down
        return moves