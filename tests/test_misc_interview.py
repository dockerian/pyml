"""
# test_misc_interview.py

"""
import logging
import os
import unittest
import sys

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class InterviewTests(unittest.TestCase):
    """
    InterviewTests includes all unit tests for ml.misc.interview module
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

    def test_get_2nd_largest(self):
        """
        test ml.misc.interview.get_2nd_largest
        :return:
        """
        from ml.misc.interview import get_2nd_largest

        smallest_num = -sys.maxsize
        tests = [{
            "result": 15, "input": [11, 3, 26, 15],  # positive tests and branch checks
        }, {
            "result": 999, "input": [19, 998, 999, 1324, 899, 16, 0],
        }, {
            "result": 0, "input": [18, -2, 0, -1.2, -999],
        }, {
            "result": -1.5, "input": [-2, 0, -1.5],
        }, {
            "result": -9999.5, "input": [-9999.5, -9999.5]
        }, {
            "result": None, "input": [2],  # negative tests and type checks and branch checks
        }, {
            "result": None, "input": 'string',
        }, {
            "result": None, "input": [-9999, 'string'],
        }, {
            "result": None, "input": [1, '101', '200'],
        }, {
            "result": smallest_num, "input": [smallest_num, smallest_num],  # edge tests
        }, {
            "result": -9223372036854775808, "input": [0, smallest_num-2, smallest_num-1]
        }]
        for test in tests:
            input_list = test["input"]
            expected = test["result"]
            result = get_2nd_largest(input_list)
            print(result)
            assert (result == expected)
            print("passed", test)
