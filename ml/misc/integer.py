"""
# misc/integer.py functions that are for integers
"""


def get_perfect_squares(num: int) -> list:
    """
    Get a mininum number of squares sum up to specific integer num.

    @param num: a positive integer target of squares sum.
    @return: a list of square numbers.
    """
    if num <= 0:
        return []
    squares = []
    results = []
    for i in range(1, num):
        square = i * i
        if square <= num:
            squares.append(square)
        else:
            break

    sum = num
    siz = len(squares)
    idx = siz - 1
    while idx >= 0 and sum > 0:
        n = squares[idx]
        diff = sum - n
        if diff >= 0:
            results.append(n)
            sum -= n
        else:
            idx -= 1
    # sum should be zero at this point
    return results
