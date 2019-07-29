"""
misc/bi_tree.py
"""


class BiTree:
    """
    Binary Indexed Tree is represented as an array.
    Each node of the Binary Indexed Tree stores the sum of some elements of the
    original array. The size of the Binary Indexed Tree is equal to the size of
    the original input array, denoted as n. This class use a size of n+1 for
    ease of implementation.

    How does Binary Indexed Tree work?
    The idea is based on the fact that all positive integers can be represented
    as the sum of powers of 2. For example 19 can be represented as 16 + 2 + 1.
    Every node of the BiTree stores the sum of n elements, n is a power of 2.
    For example, in the first diagram above (the diagram for getSum()), the sum
    of the first 12 elements can be obtained by the sum of the last 4 elements
    (from 9 to 12) plus the sum of 8 elements (from 1 to 8). The number of set
    bits in the binary representation of a number n is O(Logn). Therefore, we
    traverse at-most O(Logn) nodes in both getSum() and update() operations.
    The time complexity of the construction is O(nLogn) as it calls update()
    for all n elements.

    See
    - https://www.geeksforgeeks.org/binary-indexed-tree-or-fenwick-tree-2/
    - https://blog.csdn.net/Yaokai_AssultMaster/article/details/79492190
    """
    def __init__(self, array: list):
        n = len(array)
        # create and initialize BiTree data as all zeroes list
        self.data = [0]*(n+1)
        self.list = array

        # store the actual values in BiTree
        for i in range(n):
            self.update(i, array[i])
        pass

    def get(self, index: int):
        return self.list[index]  # if index < len(self.list) and index >= 0 else None

    def getsum(self, index: int):
        """
        Returns sum of a sub array [0..index-1].
        """
        sum = 0  # initialize result
        # BiTree index is 1 more than the index in original list.
        ndx = index + 1
        # traverse ancestors of BiTree data[index]
        while ndx > 0:
            # add current element of BiTree to sum
            sum += self.data[ndx]
            # get index of parent node
            ndx -= ndx & (-ndx)
        return sum

    def update(self, index: int, value: int):
        """
        Updates a note in Binary Index Tree (BiTree) at given list index, which
        will add given value to the data index position of BiTree and all of its
        ancestors in tree.
        """
        # BiTree index is 1 more than the index in original list.
        ndx = index + 1
        # traverse all ancestors and update the value
        while ndx > 0:
            # add value to current node of BiTree
            self.data[ndx] += value
            # get index of parent node
            ndx -= ndx & (-ndx)
        self.list[index] = value
