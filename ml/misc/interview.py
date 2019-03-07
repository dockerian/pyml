"""
interview.py functions that are for interview practice
"""


def get_2nd_largest(num_list):
    """
    Get the second largest number in a list of numbers
    :param num_list: list of numbers, list
    :return:
    """
    if not isinstance(num_list, list):
        return None
    m1st = None
    m2nd = None
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
