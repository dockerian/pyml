"""
ml/misc/grid.py
"""
import copy


class Grid:
    '''
    Grid is an N x M grid of "alive" or "dead" grid cells.

    A transformation on the input grid using the following rules:
    - An "alive" cell remains alive if 2 or 3 neighbors are "alive";
      otherwise, it becomes "dead."
    - A "dead" cell becomes alive if exactly 3 neighbors are "alive";
      otherwise, it remains "dead."
    - The term "neighbor" refers to the at-most-8 adjacent cells
      horizontally, vertically, and diagonally.

    @example: Suppose x is alive and o is dead
    * initial state:
        oooooooooo
        oooxxooooo
        ooooxooooo
        oooooooooo
        oooooooooo
    * next transforming state:
        oooooooooo
        oooxxooooo
        oooxxooooo
        oooooooooo
        oooooooooo
    '''

    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)  # grid matrix is a list of list
        self.size_col = len(grid[0])
        self.size_row = len(grid)
        # print('grid [%d, %d]: %s' % (self.size_col, self.size_row, self.grid))

    def _get_next_cell_state(self, row, col):
        """
        Return next state (0 or 1) for a cell.
        """
        current_state = self.grid[row][col]
        count = 0
        for i in [-1, 0, 1]:
            dx = col + i
            for j in [-1, 0, 1]:
                dy = row + j
                neighbor = not (dx == col and dy == row)
                ranged = 0 <= dx and dx < self.size_col and 0 <= dy and dy < self.size_row
                if ranged and neighbor:
                    # print("grid[%d,%d], neighbor[%d,%d] = %d" % (row, col, dy, dx, self.grid[dy][dx]))
                    count += self.grid[dy][dx]
        new_state = current_state
        if current_state == 1:
            if not (count >= 2 and count <= 3):
                new_state = 0
        elif count == 3:
            new_state = 1
        # print('> current: %d => new: %d, count [%d,%d] = %d' % (current_state, new_state, row, col, count))
        return new_state

    def get_next_grid_states(self):
        next = copy.deepcopy(self.grid)
        for i in range(self.size_row):
            for j in range(self.size_col):
                next[i][j] = self._get_next_cell_state(i, j)
        return next

    def is_stable(self):
        changing = False
        nextgrid = self.get_next_grid_states()
        for i in range(self.size_row):
            for j in range(self.size_col):
                if nextgrid[i][j] != self.grid[i][j]:
                    changing = True
                    break
        return not changing
