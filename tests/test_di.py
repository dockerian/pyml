"""
digiIslands tests
"""
import unittest

from ml.digiIslands.di import DigiIslands
from tests.test_di_data import TEST_DATA


class TestDigiIslands(unittest.TestCase):
    """
    DigiIslands Test
    """
    def setUp(self):
        """
        test setup
        """
        self.tests = TEST_DATA
        pass

    def test_build_islands(self):
        """
        test build_islands function
        """
        print("test DigiIslands")
        for idx, test in enumerate(self.tests):
            biggest_size = test["biggest"]
            num_of_islands = test["num"]
            matrix = test["data"]
            di = DigiIslands(matrix)
            print("Test {:02d} | O({} / {}) | {}".format(
                idx, di.bigO, di.bigO_exec, di.str()))
            self.assertEqual(di.biggest_size, biggest_size)
            self.assertEqual(di.num, num_of_islands)
            print("")

    def test_exceptions(self):
        tests = [
            "",
            None,
            "this is a string",
            {"a": 1, "b": 2, "c": 3},
            [1, 2, 3, 4],
        ]
        for test in tests:
            with self.assertRaises(TypeError) as context:
                DigiIslands(test)
            self.assertEqual(
                str(context.exception),
                'matrix must be a non-empty list of list.')

        di = DigiIslands([[]])
        di.print_islands()
