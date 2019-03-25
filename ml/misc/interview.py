"""
interview.py functions that are for interview practice
"""

from ml.utils.logger import get_logger
import array

LOGGER = get_logger(__name__)


def get_2nd_largest(num_list):
    """
    Get the second largest number in a list of numbers
    @param num_list: list of numbers, list
    @return:
    """
    if not isinstance(num_list, list):
        return None
    m1st, m2nd = None, None
    counter = 0
    for item in num_list:
        if not isinstance(item, (int, float)):
            continue
        if m2nd is None or item > m2nd:
            m2nd = item
        if m1st is None or item > m1st:
            m2nd = m1st
            m1st = item
        counter += 1
    if counter < 2:
        return None
    return m2nd


def get_fibonacci(n):
    """
    return Nth fibonacci number. Advanced: can you do BigO(1)?  O = O(n)
    Since fibonacci function is (A**n-B**n)/(5**(0.5)), where A = (1+5**1/2)/2, and B = (1-5**(1/2))/2,
    therefore it has to be O(n)
    @param n: Nth fibonacci number, ints
    @return: n'th fibonacci number
    """
    if not isinstance(n, int):
        LOGGER.info('Input not including int')
        return None
    if n < 0:
        return None
    if n == 0:
        return 0
    f0, f1, result = 0, 1, 1
    while n > 1:
        result = f0 + f1
        f0, f1 = f1, result
        n -= 1
    return result


def parse_number(input_string, parsing_hex=False):
    """
    # hex: ABCDEF
    # atoi (int, float), integer/float
    @param input_string: input string
    @param parsing_hex: ABCDEF
    @return:
    """
    input_string = str(input_string).strip().strip('+').rstrip('.')
    result, multiplier, division = 0, 10, 1
    sign = -1 if input_string and input_string[0] == '-' else 1
    if sign == -1:
        input_string = input_string.strip('-')
    for item in input_string:
        # print('ch:', item)
        if item == '.':
            if division > 1:
                return None
            multiplier, division = 1, 10
        elif item < '0' or item > '9':
            return None
        elif item >= '0' and item <= '9':
            v = ord(item) - ord('0')
            div = v / division if division > 1 else v
            result = result * multiplier + div
            # print(s, v, result)
            if division != 1:
                division *= 10

    return None if input_string == '' else result * sign


def find_largest_in_array(input_array):
    """
    find the largest element in an array
    @param input_array: input array, array
    @return: the largest number in array
    """
    if not isinstance(input_array, array.array):
        raise TypeError
    if len(input_array) == 0:
        return None
    largest = None
    for item in input_array:
        if largest is None or item > largest:
            largest = item
    return largest


def get_factorial(input_int):
    """
    compute the factorial of input_int
    @param input_int: int to be computed, ints
    @return: factorial of input number, ints
    """
    if not isinstance(input_int, int):
        LOGGER.info('input need to be an int')
        raise TypeError
    if input_int < 0:
        LOGGER.info('factorial() not defined for negative values')
        raise ValueError
    if input_int == 0:
        return 1
    else:
        return input_int * (get_factorial(input_int - 1))


def is_factorial(input_int):
    """
    check if the input int is factorial
    @param input_int: the number to be checked, ints
    @return: True or False
    """
    if not isinstance(input_int, int):
        return False
    if input_int < 0:
        return False
    result = 0
    while result <= input_int:
        if get_factorial(result) == input_int:
            return True
        result += 1
    return False


def parse_int(input):
    """
    parse the integer in the input string
    @param input: inputs that can be converted to strings
    @return:
    """
    sign, result = 1, 0
    input_string = str(input).strip().lstrip('+')
    if input_string != '' and input_string[0] == '-':
        input_string, sign = input_string[1:], -1
    for ch in input_string:
        if not '0' <= ch <= '9':
            return None
        result = 10*result + (ord(ch) - ord('0'))
    return result*sign if input_string != '' else None
