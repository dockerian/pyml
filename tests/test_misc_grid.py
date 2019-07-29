"""
# test_misc_grid.py

"""
import logging
import unittest

from ml.misc.grid import Grid
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class GridTests(unittest.TestCase):
    """
    GridTests includes all unit tests for ml.misc.grid module
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

    def test_get_next_grid_states(self):
        """
        test.ml.misc.grid :: Grid :: get_next_grid_states
        """
        tests = [{
            "init": [
              [1, 0, 1, 0],
              [0, 1, 1, 0],
              [1, 0, 0, 1],
            ],
            "next": [
              [0, 0, 1, 0],
              [1, 0, 1, 1],
              [0, 1, 1, 0],
            ],
        }, {
            "init": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "next": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        }, {
            "init": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "next": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        }]
        for idx, test in enumerate(tests):
            init = test.get("init")
            expected = test.get("next")
            grid = Grid(init)
            result = grid.get_next_grid_states()
            nextg2 = grid.get_next_grid()  # better solution
            msg = 'Test %2d |\nexpected: %s\n  result: %s' % (idx, expected, result)
            self.assertListEqual(result, expected, msg)
            self.assertListEqual(nextg2, expected, msg)

            next_grid = Grid(result)
            next_result = next_grid.get_next_grid_states()
            expected = not next_grid.is_stable()
            msg = 'Test %2d |\n changed: %s\n  result: %s' % (idx, next_result, result)
            changed = str(result) != str(next_result)
            self.assertEqual(changed, expected, msg)
        pass
