"""
# test_misc_stack.py

"""
import logging
import os
import unittest
import sys

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class StackTests(unittest.TestCase):
    """
    StackTests includes all unit tests for ml.misc.stack module
    """
    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.repo_path = os.path.dirname(self.test_path)
        self.proj_path = os.path.join(self.repo_path, "ml")
        self.base_path = os.path.join(self.repo_path, "ml", "misc")
        self.data_path = os.path.join(self.repo_path, "ml", "misc", "datasets")
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test__init__(self):
        """
        test.ml.misc.stack :: Stack :: __init__
        @return:
        """
        from ml.misc.stack import Stack
        tests = [{
            "input": [6, 77, 789, -5, 99.8], "head": [6, 77, 789, -5, 99.8],
        }, {
            "input": [[1, 32], 'string', 'string2', -3.14159, int, {'data': float}],
            "head": [[1, 32], 'string', 'string2', -3.14159, int, {'data': float}],
        }, {
            "input": [sys.maxsize], "head": [sys.maxsize],
        }, {
            "input": [-sys.maxsize], "head": [-sys.maxsize],
        }, {
            "input": [0, 0.0], "head": [0, 0.0],
        }, {
            "input": [], "head": [],
        }, {
            "input": 8, "head": [],
        }, {
            "input": int, "head": [],
        }, {
            "input": {'data': 132, 'None': None}, "head": [],
        }, {
            "input": 8.9, "head": [],
        }, {
            "input": 'string', "head": [],
        }]
        for test in tests:
            init_list = test["input"]
            expected_head = test["head"]
            obj = Stack(init_list)
            self.assertEqual(obj.stack, expected_head)

    def test_is_empty(self):
        """
        test ml.misc.stack :: Stack :: is_empty
        @return:
        """
        from ml.misc.stack import Stack
        tests = [{
            "head": [], "result": True,
        }, {
            "head": [99], "result": False,
        }, {
            "head": ['string'], "result": False,
        }, {
            "head": [64, -99.343, 0, sys.maxsize, -sys.maxsize], "result": False,
        }, {
            "head": 0, "result": False
        }, {
            "head": 'string', "result": False,
        }, {
            "head": float, "result": False
        }, {
            "head": {}, "result": False,
        }, {
            "head": None, "result": False,
        }]
        for test in tests:
            head = test["head"]
            expected = test["result"]
            obj = Stack()
            obj.stack = head
            result = obj.is_empty()
            self.assertEqual(result, expected)

    def test_peek(self):
        """
        test ml.misc.stack :: Stack :: peek
        test ml.misc.stack :: QueueStack :: peek
        @return:
        """
        from ml.misc.stack import Stack, QueueStack
        tests = [{
            "input": [6, 77, 789, -5, 99.8], "result": 99.8,
        }, {
            "input": [[1, 32], 'string', 'string2', -3.14159, int, {'data': float}],
            "result": {'data': float},
        }, {
            "input": [sys.maxsize], "result": sys.maxsize,
        }, {
            "input": [-sys.maxsize], "result": -sys.maxsize,
        }, {
            "input": [0, 0.0], "result": 0.0,
        }, {
            "input": [], "result": None,
        }, {
            "input": 8, "result": None,
        }, {
            "input": int, "result": None,
        }, {
            "input": {'data': 132, 'None': None}, "result": None,
        }, {
            "input": 8.9, "result": None,
        }, {
            "input": 'string', "result": None,
        }]
        for test in tests:
            init_list = test["input"]
            expected = test["result"]
            obj = Stack(init_list)
            result = obj.peek()
            self.assertEqual(result, expected)  # test Stack
            obj_2 = QueueStack()
            obj_2.from_list(init_list)
            result_2 = obj_2.peek()
            self.assertEqual(result_2, expected)  # test QueueStack

    def test_pop(self):
        """
        test.ml.misc.stack :: Stack :: pop
        test.ml.misc.stack :: QueueStack :: pop
        @return:
        """
        from ml.misc.stack import Stack, QueueStack
        tests = [{
            "input": [3, 3.7, 56.98, -934, 0.765],
            "head": [3, 3.7, 56.98, -934],
            "result": 0.765,
        }, {
            "input": [1995, 'string', 0],
            "head": [1995, 'string'],
            "result": 0
        }, {
            "input": [3761],
            "head": [],
            "result": 3761,
        }, {
            "input": [],
            "head": [],
            "result": None,
        }, {
            "input": 'string',
            "head": [],
            "result": None,
        }, {
            "input": -12.3,
            "head": [],
            "result": None,
        }, {
            "input": int,
            "head": [],
            "result": None,
        }]
        for test in tests:
            if isinstance(test["input"], list):
                init_list = test["input"].copy()
            else:
                init_list = test["input"]
            expected_head = test["head"]
            expected = test["result"]
            obj = Stack(init_list)
            result = obj.pop()
            self.assertListEqual(obj.stack, expected_head)  # test Stack
            self.assertEqual(result, expected)
            if isinstance(test["input"], list):
                init_list_2 = test["input"].copy()
            else:
                init_list_2 = test["input"]
            obj_2 = QueueStack()
            obj_2.from_list(init_list_2)
            result_2 = obj_2.pop()
            self.assertListEqual(obj_2.q1.queue, expected_head)  # test QueueStack
            self.assertEqual(result_2, expected)

    def test_push(self):
        """
        ml.misc.stack :: Stack :: push
        ml.misc.stack :: StackQueue :: push
        @return:
        """
        from ml.misc.stack import Stack, QueueStack
        tests = [{
            "list": [1314, 732, -sys.maxsize, 99.8],
            "input": 0.0,
            "head": [1314, 732, -sys.maxsize, 99.8, 0.0],
        }, {
            "list": [0.98, 'string'],
            "input": 0,
            "head": [0.98, 'string', 0],
        }, {
            "list": [7],
            "input": float,
            "head": [7, float],
        }, {
            "list": [0],
            "input": 'string',
            "head": [0, 'string'],
        }, {
            "list": [45, 'string'],
            "input": ['string1', 'string2'],
            "head": [45, 'string', ['string1', 'string2']],
        }, {
            "list": [77],
            "input": {'data': [0.0, 0]},
            "head": [77, {'data': [0.0, 0]}],
        }, {
            "list": [75.5],
            "input": None,
            "head": [75.5, None]
        }, {
            "list": [],
            "input": sys.maxsize,
            "head": [sys.maxsize],
        }, {
            "list": [],
            "input": -sys.maxsize,
            "head": [-sys.maxsize]
        }, {
            "list": None,
            "input": 'string',
            "head": ['string'],
        }, {
            "list": float,
            "input": int,
            "head": [int],
        }, {
            "list": 123,
            "input": 321,
            "head": [321],
        }, {
            "list": 33.3,
            "input": None,
            "head": [None],
        }, {
            "list": None,
            "input": None,
            "head": [None],
        }]
        for test in tests:
            if isinstance(test["list"], list):
                init_list = test["list"].copy()
            else:
                init_list = test["list"]
            item = test["input"]
            expected_head = test["head"]
            obj = Stack(init_list)
            obj.push(item)
            self.assertListEqual(obj.stack, expected_head)  # test Stack
            if isinstance(test["list"], list):
                init_list_2 = test["list"].copy()
            else:
                init_list_2 = test["list"]
            obj_2 = QueueStack()
            obj_2.from_list(init_list_2)
            obj_2.push(item)
            self.assertListEqual(obj_2.q1.queue, expected_head)  # test QueueStack\
