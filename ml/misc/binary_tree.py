"""
misc/binary_tree.py
"""
import json


class BinaryTree:

    def __init__(self):
        self.root = {}
        self.height = 0  # the longest path from the root to its leaves
        pass

    def deserialize(self, encoded: str):
        arr = json.loads(encoded)
        if isinstance(arr, list):
            return from_preorder(arr)
        raise Exception('Invalid data: encoded BinaryTree must be a list')

    def serialize(self) -> str:
        arr = to_preorder()
        encoded = json.dumps(arr, sort_keys=True)
        return encoded


def from_inorder(arr: list) -> dict:
    """
    Convert an array to tree, returning the root node.
    """
    node = None
    size = len(arr)
    if size > 0 and arr[0] is not None:
        node = {}
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
    Convert an array to tree, returning the root node.
    """
    node = None
    size = len(arr)
    if size > 0 and arr[0] is not None:
        node = {}
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
    Convert an array to tree, returning the root node.
    """
    node = None
    size = len(arr)
    if size > 0 and arr[0] is not None:
        node = {}
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
    if data is None or not isinstance(data, list):
        data = []
    value = node.get('value') if node else None
    if node:
        to_inorder(node.get('left'), data)
        data.append(value)
        to_inorder(node.get('right'), data)
    elif data and value:
        data.append(None)
    return data


def to_postorder(node: dict, data: list=None):
    if data is None or not isinstance(data, list):
        data = []
    value = node.get('value') if node else None
    if node:
        to_postorder(node.get('left'), data)
        to_postorder(node.get('right'), data)
        data.append(value)
    elif data and value:
        data.append(None)
    return data


def to_preorder(node: dict, data: list=None):
    if data is None or not isinstance(data, list):
        data = []
    value = node.get('value') if node else None
    if node:
        data.append(value)
        to_preorder(node.get('left'), data)
        to_preorder(node.get('right'), data)
    elif data:
        data.append(None)
    return data
