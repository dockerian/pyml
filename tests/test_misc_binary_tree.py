"""
# test_misc_grid.py

"""
import logging
import unittest

from ml.misc.binary_tree import \
    from_breadth_first, breadth_first, \
    from_inorder, to_inorder, to_inorder_iterative, \
    from_preorder, to_preorder, to_preorder_iterative, \
    from_postorder, to_postorder, to_postorder_iterative, \
    BinaryTree
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class BinarytreeTests(unittest.TestCase):
    """
    BinarytreeTests includes all unit tests for ml.misc.binary_tree module
    """
    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        self.tests = [
            [],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [-10, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100, 1000],
            ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr', 'stu', 'vw', 'xyz'],
            [123, 'abcdefg', 9999, 3.14, 'xyz', 217, '3.14', 'foobar', 0],
        ]
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test_serialization(self):
        for test in self.tests:
            root = from_preorder(test)
            tree = BinaryTree()
            tree.root = from_preorder(test)
            encoded = tree.serialize()
            decoded = tree.deserialize(encoded)
            self.assertDictEqual(decoded, root)
        pass

    def test_class_exception(self):
        tree = BinaryTree()
        with self.assertRaises(Exception) as ctx:
            ctx_msg = 'Invalid data: encoded BinaryTree must be a list'
            tree.deserialize('{"key": "invalid encoded data"}')
            self.assertTrue(ctx_msg in str(ctx.exception), "should raise exception")

        from json import JSONDecodeError
        with self.assertRaises(Exception) as ctx:
            tree.deserialize('invalid encoded data')
            self.assertIsInstance(ctx.exception, JSONDecodeError)

    def test_methods(self):
        for test in self.tests:
            obj = from_breadth_first(test)
            arr = breadth_first(obj)

            obj = from_postorder(test)
            arr = to_postorder(obj)
            self.assertListEqual(arr, test)
            arr = to_postorder_iterative(obj)
            self.assertListEqual(arr, test)

            obj = from_preorder(test)
            arr = to_preorder(obj)
            self.assertListEqual(arr, test)
            arr = to_preorder_iterative(obj)
            self.assertListEqual(arr, test)

            obj = from_inorder(test)
            arr = to_inorder(obj)
            self.assertListEqual(arr, test)
            arr = to_inorder_iterative(obj)
            self.assertListEqual(arr, test)
