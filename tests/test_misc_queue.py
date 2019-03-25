"""
# test_misc_queue.py

"""
import logging
import os
import unittest
import sys

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class QueueTests(unittest.TestCase):
    """
    QueueTests includes all unit tests for ml.misc.queue module except StackQueue
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

    def test_dequeue(self):
        """
        test.ml.misc.queue :: Queue :: dequeue
        test.ml.misc.queue :: StackQueue :: dequeue
        @return:
        """
        from ml.misc.queue import Queue, StackQueue
        tests = [{
            "list": [3, -4.5, 0, sys.maxsize, -sys.maxsize],
            "head": [3, -4.5, 0, sys.maxsize],
            "result": -sys.maxsize,
        }, {
            "list": ['string', 3001, 'string2', int],
            "head": ['string', 3001, 'string2'],
            "result": int,
        }, {
            "list": [{'type': dict}],
            "head": [],
            "result": {'type': dict},

        }, {
            "list": [],
            "head": [],
            "result": None,
        }, {
            "list": 3,
            "head": [],
            "result": None,
        }, {
            "list": 7.7,
            "head": [],
            "result": None,
        }, {
            "list": float,
            "head": [],
            "result": None,
        }, {
            "list": {'string': [dict]},
            "head": [],
            "result": None,
        }, {
            "list": None,
            "head": [],
            "result": None,
        }]
        for test in tests:
            if isinstance(test["list"], list):
                init_list = test["list"].copy()
            else:
                init_list = test["list"]
            expected_head = test["head"]
            expected = test["result"]
            obj = Queue(init_list)
            result = obj.dequeue()
            self.assertListEqual(obj.queue, expected_head)  # test Queue
            self.assertEqual(result, expected)
            if isinstance(test["list"], list):
                init_list_2 = test["list"].copy()
                init_list_2.reverse()
            else:
                init_list_2 = test["list"]
            obj_2 = StackQueue()
            obj_2.from_list(init_list_2)
            result_2 = obj_2.dequeue()
            self.assertListEqual(obj_2.s1.stack, expected_head)  # test StackQueue
            self.assertEqual(result_2, expected)

    def test_enqueue(self):
        """
        test.ml.misc.queue :: Queue :: enqueue
        test.ml.misc.queue :: StackQueue :: enqueue
        @return:
        """
        from ml.misc.queue import Queue, StackQueue
        tests = [{
            "list": [8, 8.8, 0, sys.maxsize, -sys.maxsize, 'string'],
            "input": ['list string'],
            "head": [['list string'], 8, 8.8, 0, sys.maxsize, -sys.maxsize, 'string'],
        }, {
            "list": [7.7, 0, -11],
            "input": int,
            "head": [int, 7.7, 0, -11],
        }, {
            "list": [0],
            "input": 0.0,
            "head": [0.0, 0],
        }, {
            "list": [],
            "input": 'string',
            "head": ['string'],
        }, {
            "list": 3,
            "input": 5,
            "head": [5],
        }, {
            "list": 99.8,
            "input": 3.14,
            "head": [3.14],
        }, {
            "list": 'string',
            "input": None,
            "head": [None],
        }, {
            "list": float,
            "input": 'string',
            "head": ['string'],
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
            input_item = test["input"]
            expected_head = test["head"]
            obj = Queue(init_list)
            obj.enqueue(input_item)
            self.assertEqual(obj.queue, expected_head)  # test Queue
            if isinstance(test["list"], list):
                init_list_2 = test["list"].copy()
                init_list_2.reverse()
            else:
                init_list_2 = test["list"]
            obj_2 = StackQueue()
            obj_2.from_list(init_list_2)
            obj_2.enqueue(input_item)
            self.assertEqual(obj_2.s1.stack, expected_head)

    def test_is_empty(self):
        """
        test.ml.misc.queue :: Queue :: is_empty
        @return:
        """
        from ml.misc.queue import Queue
        tests = [{
            "head": [], "result": True,
        }, {
            "head": [199], "result": False,
        }, {
            "head": ['string'], "result": False,
        }, {
            "head": [73234, -3.1415926, 0, sys.maxsize, -sys.maxsize], "result": False,
        }, {
            "head": 0, "result": False
        }, {
            "head": 0.0, "result": False
        }, {
            "head": 'string', "result": False,
        }, {
            "head": dict, "result": False
        }, {
            "head": {}, "result": False,
        }, {
            "head": None, "result": False,
        }]
        for test in tests:
            head = test["head"]
            expected = test["result"]
            obj = Queue()
            obj.queue = head
            result = obj.is_empty()
            self.assertEqual(result, expected)

    def test_peek(self):
        """
        test ml.misc.queue :: Queue :: peek
        test ml.misc.queue :: StackQueue :: peek
        @return:
        """
        from ml.misc.queue import Queue, StackQueue
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
            obj = Queue(init_list)
            result = obj.peek()
            self.assertEqual(result, expected)  # test Queue
            init_list_2 = test["input"]
            if isinstance(init_list_2, list):
                init_list_2.reverse()
            obj_2 = StackQueue()
            obj_2.from_list(init_list_2)
            result_2 = obj_2.peek()
            self.assertEqual(result_2, expected)  # test StackQueue
