"""
# misc/integer.py functions that are for integers
"""


def get_local_maxima(inputs: list) -> list:
    '''
    Find all local maxima from the input list of integers.

    Examples:
    - inputs: [11, 5, 10, 6, 4, 7, 4, 10, 1]
      output: [11, 10, 7, 10]
    - inputs: [1, 2, 1]
      output; [2]
    - inputs: [1, 2, 3, 4, 3]
      output: [4]
    - inputs: [1, 2, 3, 4, 4, 4, 4]
      output: [4]
    - inputs: [1, 4, 3, 4]
      output: [4, 4]
    '''
    prev = None
    results = []
    siz = len(inputs)
    for idx, v in enumerate(inputs):
        # larger than both neighbors, or larger than left and at the end
        larger_than_prev = prev is None or v > prev  # always True for the 1st item
        larger_than_next = v >= inputs[idx+1] if idx+1 < siz else False
        if larger_than_prev and (larger_than_next or idx == siz - 1):
            results.append(v)
        prev = v
    return results


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
