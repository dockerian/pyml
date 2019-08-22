"""
# test_misc_integer
"""
import logging
import unittest
import sys

from ml.misc.integer import get_local_maxima
from ml.misc.integer import get_perfect_squares


class MiscIntegerTester(unittest.TestCase):
    """
    MiscIntegerTester includes all unit tests for misc/integer.py
    """

    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test_get_local_maxima(self):
        tests = [{
            "input": [-1],
            "output": [-1]
        }, {
            "input": [0],
            "output": [0]
        }, {
            "input": [-sys.maxsize],
            "output": [-sys.maxsize]
        }, {
            "input": [sys.maxsize],
            "output": [sys.maxsize]
        }, {
            "input": [3, sys.maxsize, 0],
            "output": [sys.maxsize]
        }, {
            "input": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "output": [0]
        }, {
            "input": [7, 7, 7, 7, 7, 7, 7],
            "output": [7]
        }, {
            "input": [1, 2, 1],
            "output": [2]
        }, {
            "input": [-55, -2, -5],
            "output": [-2]
        }, {
            "input": [-5, 2],
            "output": [2]
        }, {
            "input": [5, 2],
            "output": [5]
        }, {
            "input": [-1, 0, 2, 100, 10000, 123456],
            "output": [123456]
        }, {
            "input": [3, 2, 1],
            "output": [3]
        }, {
            "input": [1, 2, 3],
            "output": [3]
        }, {
            "input": [1, 2, 1],
            "output": [2]
        }, {
            "input": [1, 2, 3, 4, 3],
            "output": [4]
        }, {
            "input": [1, 2, 3, 4, 4, 4, 2, 5],
            "output": [4, 5]
        }]
        for test in tests:
            expected = test["output"]
            result = get_local_maxima(test["input"])
            self.assertListEqual(result, expected)

    def test_get_perfect_squares(self):
        import random
        tests = [random.randint(1, 65535) for i in range(0, 100)]
        for test in tests:
            results = get_perfect_squares(test)
            sum_val = sum(results)
            self.assertEqual(sum_val, test)
        pass
