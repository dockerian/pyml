"""
misc/binary_tree.py
"""
import json


class BinaryTree:

    def __init__(self):
        self.root = {}
        self.height = 0  # the longest path from the root to its leaves
        pass

    def deserialize(self, encoded: str) -> dict:
        arr = json.loads(encoded)
        if isinstance(arr, list):
            return from_preorder(arr)
        raise Exception('Invalid data: encoded BinaryTree must be a list')

    def serialize(self) -> str:
        arr = to_preorder(self.root)
        encoded = json.dumps(arr, sort_keys=True)
        return encoded


def breadth_first(root: dict) -> list:
    """
    Using a queue to do breadth-first traverse from tree root iteratively.
    """
    if not root or not isinstance(root, dict):
        return []
    data = []
    node = root
    queue = []
    queue.append(node)  # enqueue the node - add the node at the end
    while len(queue) > 0:
        node = queue[0] or {}
        del queue[0]  # dequeue the node - remove the node from the beginning
        data.append(node.get('value'))
        node_left = node.get('left')
        node_right = node.get('right')
        if node_left:
            queue.append(node_left)   # enqueue the left
        if node_right:
            queue.append(node_right)  # enqueue the right
    return data


def from_breadth_first(arr: list) -> dict:
    r"""
    Reconstruct a tree from breadth-first (sorted) list.

    At each index, its potential 2 children (left and right) are at
    2 * index + 1 and 2 * index + 2.

    For example: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] represents
              0 (root)
             /     \
            1       2
           / \     / \
          3   4   5   6
         / \
        7   8
    """
    def from_sorted(arr, size, index, node):
        l_index = 2 * index + 1
        r_index = 2 * index + 2
        if index < size:
            node['value'] = arr[index]
        if l_index < size:
            node['left'] = {'value': arr[l_index]}
            from_sorted(arr, size, l_index, node['left'])
        if r_index < size:
            node['right'] = {'value': arr[r_index]}
            from_sorted(arr, size, r_index, node['right'])

    node = {}
    if isinstance(arr, list):
        size = len(arr)
        from_sorted(arr, size, 0, node)
    return node


def from_inorder(arr: list) -> dict:
    """
    Convert a depth-first in-order array to binary tree, returning the root node.
    """
    node = {}
    size = len(arr)
    if size > 0 and arr[0] is not None:
        half = size // 2
        node['value'] = arr[half]
        if half > 0:
            half_1st = from_inorder(arr[0:half])
            if half_1st:
                node['left'] = half_1st
        if half < size - 1:
            half_2nd = from_inorder(arr[half+1:size])
            if half_2nd:
                node['right'] = half_2nd
    return node


def from_postorder(arr: list) -> dict:
    """
    Convert a depth-first post-order array to binary tree, returning the root node.
    """
    node = {}
    size = len(arr)
    if size > 0 and arr[0] is not None:
        node['value'] = arr[size-1]
        half = size // 2
        if half > 0:
            half_1st = from_postorder(arr[0:half])
            if half_1st:
                node['left'] = half_1st
        if half < size - 1:
            half_2nd = from_postorder(arr[half:size-1])
            if half_2nd:
                node['right'] = half_2nd
    return node


def from_preorder(arr: list) -> dict:
    """
    Convert a depth-first pre-order array to binary tree, returning the root node.
    """
    node = {}
    size = len(arr)
    if size > 0 and arr[0] is not None:
        node['value'] = arr[0]
        half = (size // 2) + 1
        if half > 1:
            half_1st = from_preorder(arr[1:half])
            if half_1st:
                node['left'] = half_1st
        if half < size:
            half_2nd = from_preorder(arr[half:size])
            if half_2nd:
                node['right'] = half_2nd
    return node


def to_inorder(node: dict, data: list=None):
    r"""
    Convert a binary tree node to depth-first in-order list.

    Example:
        ```
              F (root)
             /       \
            C         I
           /  \      /  \
          B    E    H    J
         /    /    /    /
        A    D    G    K
        ```
    """
    if data is None or not isinstance(data, list):
        data = []
    if node:
        to_inorder(node.get('left'), data)
        data.append(node.get('value'))
        to_inorder(node.get('right'), data)
    return data


def to_inorder_iterative(root: dict) -> list:
    """
    Convert a binary tree node to depth-first in-order list (iteratively).
    """
    node = root
    node_list = []
    stack = []
    while node or len(stack) > 0:
        if node:
            stack.append(node)  # push a node into the stack
            node = node.get('left')
        else:
            node = stack[-1]
            del stack[-1]   # pop the node from stack
            node_value = node.get('value')
            if node_value is not None:
                node_list.append(node_value)
            node = node.get('right')
    return node_list


def to_postorder(node: dict, data: list=None):
    r"""
    Convert a binary tree node to depth-first post-order list.

    Example:
        ```
              K (root)
             /       \
            E         J
           /  \      /  \
          B    D    G    I
         /    /    /    /
        A   C     F    H
        ```
    """
    if data is None or not isinstance(data, list):
        data = []
    if node:
        to_postorder(node.get('left'), data)
        to_postorder(node.get('right'), data)
        data.append(node.get('value'))
    return data


def to_postorder_iterative(root: dict) -> list:
    """
    Convert a binary tree node to depth-first post-order list (iteratively).
    """
    node, node_list, stack = root, [], []
    stack.append(node)  # push root into the stack
    while len(stack) > 0:
        node = stack[-1]
        del stack[-1]   # pop the node from stack
        node_left = node.get('left')
        node_right = node.get('right')
        node_value = node.get('value')
        if node_value is not None:
            node_list.insert(0, node_value)
        if node_left:
            stack.append(node_left)   # push the left into the stack
        if node_right:
            stack.append(node_right)  # push the right into the stack
    return node_list


def to_preorder(node: dict, data: list=None):
    r"""
    Convert a binary tree node to depth-first pre-order list.

    Example:
        ```
            A (root)
           /       \
          B         G
         /  \      /  \
        C    E    H    J
       /    /    /    /
      D    F    I    K
        ```
    """
    if data is None or not isinstance(data, list):
        data = []
    if node:
        data.append(node.get('value'))
        to_preorder(node.get('left'), data)
        to_preorder(node.get('right'), data)
    return data


def to_preorder_iterative(root: dict) -> list:
    """
    Convert a binary tree node to depth-first pre-order list (iteratively).
    """
    node, node_list, stack = root, [], []
    stack.append(node)  # push root into the stack
    while len(stack) > 0:
        node = stack[-1]
        del stack[-1]   # pop the node from stack
        node_left = node.get('left')
        node_right = node.get('right')
        node_value = node.get('value')
        if node_value is not None:
            node_list.append(node_value)
        if node_right:
            stack.append(node_right)  # push the right into the stack
        if node_left:
            stack.append(node_left)   # push the left into the stack
    return node_list
