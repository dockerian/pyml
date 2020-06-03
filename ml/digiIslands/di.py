"""
class DigiIslands
"""
import ml.utils.extension as utils

COORD_X = 0  # index of coordinate x
COORD_Y = 1  # index of coordinate y
LANDTAG = 1  # value to indicate solid land


class DigiIslands:
    """
    DigiIslands uses input from a 2D matrix to build representation of digital islands.
    """

    def __init__(self, matrix: list):
        """Construct a DigiIslands object."""
        if not isinstance(matrix, list) or \
                len(matrix) < 1 or \
                not isinstance(matrix[0], list):
            raise TypeError("matrix must be a non-empty list of list.")
        self.data = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
        self.num = 0  # number of islands
        self._b = []  # boundary of 2 coordinates [x, y] as top-left and bottom-right corners, slice of slices
        self._m = []  # group of coords [x, y] to represent land digits, slice of slices
        self._v = [
            [False for _ in range(self.cols)] for _ in range(self.rows)
        ]  # visited coords
        self.bigO = 0  # big O(n) of calculation
        self.bigO_exec = 0  # big O(n) of statements
        self.biggest_size = 0
        self.biggest_island_index = None
        self.build_islands()

    def __str__(self):
        """String method"""
        return utils.str_matrix(self._m)

    def build_islands(self):
        """
        Build islands from matrix data.
        """
        for x in range(self.rows):
            for y in range(self.cols):
                if self._v[x][y]:
                    continue
                self.bigO += 1
                self.bigO_exec += 1
                if self.data[x][y] == LANDTAG:
                    self.join_islands(x, y)
                self._v[x][y] = True
        # self.print_islands()
        pass

    def check_surroundings(self, x, y, g):
        """
        Check surrounding coords of (x, y) to join group g.
        """
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.bigO_exec += 1
                a, b = x + dx, y + dy
                if (a == x and b == y) or \
                    a < 0 or a >= self.rows or \
                    b < 0 or b >= self.cols or \
                        self._v[a][b]:
                    # print("- skip [{}, {}]".format(a, b))
                    continue
                # print("- check surrounding ({}, {}) of ({}, {}) for group {}".format(a, b, x, y, g))
                self.bigO += 1
                if self.data[a][b] == LANDTAG:
                    self.join_islands(a, b, g)
                self._v[a][b] = True
        pass

    def join_islands(self, x, y, g=None):
        """
        Join a coordinate (x, y) to a group.
        """
        # print("- join ({}, {}) to group {}".format(x, y, g))
        # check boundary
        if g is None:
            g, self.num = self.num, self.num + 1
            self._m.append([])

        self._m[g].append([x, y])  # add to the group
        self._v[x][y] = True

        # check biggest island
        if len(self._m[g]) > self.biggest_size:
            self.biggest_size = len(self._m[g])
            self.biggest_island_index = g

        # create or update bounary
        self.set_boundary(x, y, g)

        # check surrounding coords of (x, y)
        self.check_surroundings(x, y, g)
        pass

    def print_islands(self):
        print("- built islands ({}, biggest size {}): {}".format(
            self.num, self.biggest_size, self))

    def set_boundary(self, x, y, g):
        """
        Create or update boundary of a group at coord (x, y).
        """
        if g >= len(self._b):
            # print("- create new boundary [{}]({}, {})".format(g, x, y))
            self._b.append([[x, y], [x, y]])
            return

        # print("- update boundary {} at ({}, {}) - len(g)={}".format(g, x, y, len(self._b)))
        # get top-left and bottom-right
        tl, br = self._b[g][0], self._b[g][1]
        tl[COORD_X] = x if x < tl[COORD_X] else tl[COORD_X]
        tl[COORD_Y] = y if y < tl[COORD_Y] else tl[COORD_Y]
        br[COORD_X] = x if x > br[COORD_X] else br[COORD_X]
        br[COORD_Y] = y if y > br[COORD_Y] else br[COORD_Y]
        # self._b[g] = [tl, br]
        pass

    def str(self):
        return "digiIslands [{}x{}] ({}, biggest size {}): {}".format(
            self.rows, self.cols, self.num, self.biggest_size, self)
