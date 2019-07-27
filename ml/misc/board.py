"""
misc/board.py
"""


def check_connect_4(board: list, x: int, y: int) -> int:
    """
    @param board: the board data.
    @param x: column index.
    @param y: row index.
    """
    rows = len(board)
    cols = len(board[0])
    tile = board[y][x]

    i, j, count = y-1, y+1, 1
    while i >= 0 or j < rows:
        count += 1 if i >= 0 and board[i][x] == tile else 0
        count += 1 if j < rows and board[j][x] == tile else 0
        i -= 1
        j += 1
    if count >= 4:
        return count

    i, j, count = x-1, x+1, 1
    while i >= 0 or j < cols:
        count += 1 if i >= 0 and board[y][i] == tile else 0
        count += 1 if j < cols and board[y][j] == tile else 0
        i -= 1
        j += 1
    if count >= 4:
        return count

    i, j, count = x-1, y-1, 1
    while i >= 0 and j >= 0:
        count += 1 if board[j][i] == tile else 0
        count += 1 if board[j][i] == tile else 0
        i -= 1
        j -= 1
    i, j = x+1, y+1
    while i < cols and j < rows:
        count += 1 if board[j][i] == tile else 0
        count += 1 if board[j][i] == tile else 0
        i += 1
        j += 1
    if count >= 4:
        return count

    return 0


def check_connect_4_board(board: list):
    """
    Connect-Four Board State Checker

    The program or function must take in a Connect 4 board and return true if
    the board is valid and false if it is not. It is okay to assume whatever
    board representation you like (e.g. Array of Arrays).

    The Rules For Connect 4:
    - Players R and Y take it in turns to drop tiles of their colour into
    columns of a 7x6 grid. When a player drops a tile into the column, it falls
    down to occupy the lowest unfilled position in that column. If a player
    manages to get a horizontal, vertical or diagonal run of four tiles of
    their colour on the board, then they win and the game ends immediately.

    For example (with R starting), the following are an impossible Connect 4 position.

    | | | | | | | |
    | | | | | | | |
    | | | | | | | |
    | | |R| | | | |
    | | |Y| | | | |
    |R| |Y| | | | |

    | | | | | | | |
    | | | | | | | |
    | | | | | | | |
    | | | | | | | |
    | |Y|Y|Y|Y| | |
    | |R|R|R|R| | |

    And some possible states:

    | | | | | | | |
    | | | | | | | |
    | | | | | | | |
    | | |R| | | | |
    | | |Y| | | | |
    |R|R|Y| | | | |

    | | | | | | | |
    | | |Y| | | | |
    | | |R| | | | |
    | | |Y| | | | |
    | | |R| | | | |
    | |Y|R| | | | |

    """
    rows = len(board)
    cols = len(board[0])
    count_r = 0
    count_y = 0
    stacks = {}
    for col in range(cols):
        stacks[col] = []
        for row in range(rows):
            tile = board[row][col]
            if tile == 'R':
                count_r += 1
                stacks[col].insert(0, 'R')
                continue
            if tile == 'Y':
                count_y += 1
                stacks[col].insert(0, 'Y')
                continue

    last_tile = 'R' if count_r > count_y else 'Y'

    if not (last_tile == 'R' and count_r == count_y + 1):
        return False
    if not (last_tile == 'Y' and count_r == count_y):
        return False

    remove = last_tile
    count = count_r + count_y

    while count > 0:
        for col in range(cols):
            stack = stacks[col]
            if stack[-1] == remove:
                del stack[-1]
                remove = 'R' if remove == 'Y' else 'Y'
                count -= 1
                break

    if count > 0:
        return False

    return True
