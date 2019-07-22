"""
# test_misc_integer
"""
import logging
import unittest

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

    def test_get_perfect_squares(self):
        import random
        tests = [random.randint(1, 65535) for i in range(0, 100)]
        for test in tests:
            results = get_perfect_squares(test)
            sum_val = sum(results)
            self.assertEqual(sum_val, test)
        pass
