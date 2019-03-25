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
        @return:
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

    def test_get_fibonacci(self):
        """
        test ml.misc.interview.get_fibonacci
        @return:
        """
        from ml.misc.interview import get_fibonacci
        tests = [{
            "result": 1, "n": 2,
        }, {
            "result": 218922995834555169026, "n": 99,
        }, {
            "result": 0, "n": 0,
        }, {
            "result": None, "n": 'string',
        }, {
            "result": None, "n": [1, 2, 3],
        }, {
            "result": None, "n": -8.5,
        }, {
            "result": None, "n": 159.29,
        }, {
            "result": None, "n": -5,
        }]

        for test in tests:
            n = test['n']
            expected = test['result']
            result = get_fibonacci(n)
            self.assertEqual(result, expected)

    def test_parse_number(self):
        """
        test ml.misc.interview.parseNumber
        @return:
        """
        from ml.misc.interview import parse_number
        tests = [{
            "result": 0, "in": '   0    ',
        }, {
            "result": None, "in": '               99string    ',
        }, {
            "result": None, "in": '3838438sanba   ',
        }, {
            "result": 3.1415926, "in": '     3.1415926',
        }, {
            "result": None, "in": '-57perfectstring   ',
        }, {
            "result": None, "in": '   +789uuueeexddd  ',
        }, {
            "result": None, "in": '   abcd998     ',
        }, {
            "result": 96, "in": '96'
        }, {
            "result": 9.89, "in": '9.89',
        }, {
            "result": None, "in": ['3', '4', 'ade', 'lol', 'dota2'],
        }, {
            "result": None, "in": None,
        }, {
            "result": None, "in": '      ',
        }, {
            "result": None, "in": '',
        }, {
            "result": None, "in": '+',
        }, {
            "result": None, "in": "-",
        }, {
            "result": None, "in": '3.14.15926'
        }]
        for test in tests:
            input_string = test['in']
            expected = test['result']
            result = parse_number(input_string)
            if isinstance(result, float):
                self.assertTrue(abs(result - expected) < .0000001)
            else:
                self.assertEqual(result, expected)

    def test_find_largest_in_array(self):
        """
        test ml.misc.interview.find_largest_in_array
        @return:
        """
        import array

        from ml.misc.interview import find_largest_in_array
        tests = [{
            "result": 98,
            "my_array": array.array('b', [3, 98, -77, 66]),
        }, {
            "result": 122,
            "my_array": array.array('B', [122, 54, 23, 0]),
        }, {
            "result": 0,
            "my_array": array.array('h', [-32767, -98, -77, -66, 0]),
        }, {
            "result": 32767,
            "my_array": array.array('H', [3, 98, 77, 32767]),
        }, {
            "result": -7,
            "my_array": array.array('i', [-7]),
        }, {
            "result": None,
            "my_array": array.array('I'),
        }, {
            "result": -98765,
            "my_array": array.array('l', [-84758453534, -3761582984123, -4344574573984, -98765]),
        }, {
            "result": 4344574573984,
            "my_array": array.array('L', [84758453534, 3761582984123, 4344574573984, 98765]),
        }, {
            "result": 3.1415926,
            "my_array": array.array('d', [-0.00001, -99, 1.5, 3.1415926]),
        }]
        for test in tests:
            input_array = test['my_array']
            expected = test['result']
            result = find_largest_in_array(input_array)
            self.assertEqual(result, expected)

        # testing floats
        tests_float = [{
            "result": 6.748237609863281,
            "my_array":  array.array('f', [-0.01, 0.1, 6.74823742, 0]),
        }, {
            "result": -8.437568664550781,
            "my_array": array.array('f', [-99.76, -56743.843275, -8.4375683453423, -10.23431123]),
        }]
        for test in tests_float:
            input_array = test['my_array']
            expected = test['result']
            result = find_largest_in_array(input_array)
            self.assertTrue(abs(expected-result) < 0.0001)

        # exception check
        tests_ex = [{
            "my_array": 5,
        }, {
            "my_array": [1, 3, 9],
        }, {
            "my_array": {'data': 0, 'next': None}
        }, {
            "my_array": None,
        }, {
            "my_array": 'string',
        }]
        for test in tests_ex:
            input_array = test['my_array']
            with self.assertRaises(TypeError):
                find_largest_in_array(input_array)

    def test_get_factorial(self):
        """
        test ml.misc.interview.get_fatorial
        @return:
        """
        from ml.misc.interview import get_factorial
        large_int_1 = 30414093201713378043612608166064768844377641568960512000000000000
        tests = [{
            "result": 120, "num": 5,
        }, {
            "result": 362880, "num": 9,
        }, {
            "result": large_int_1, "num": 50,
        }, {
            "result": 1, "num": 0,
        }, {
            "result": 1, "num": 1,
        }]
        for test in tests:
            my_num = test['num']
            expected = test['result']
            result = get_factorial(my_num)
            self.assertEqual(result, expected)
        # exception checks
        tests_ex = [{
            "num": 6.7,
        }, {
            "num": int,
        }, {
            "num": -3,
        }, {
            "num": None,
        }, {
            "num": 'string',
        }, {
            "num": 1.0
        }, {
            "num": [1, 8, 7]
        }, {
            "num": {'data': 1, 'next': None}
        }]

        for test in tests_ex:
            my_num = test['num']
            with self.assertRaises(Exception):
                get_factorial(my_num)

    def test_is_factorial(self):
        """
        test ml.misc.interview.is_factorial
        @return:
        """
        from ml.misc.interview import is_factorial
        tests = [{
            "result": True, "num": 120
        }, {
            "result": True, "num": 24,
        }, {
            "result": True, "num": 479001600,
        }, {
            "result": True, "num": 40320,
        }, {
            "result": False, "num": 3,
        }, {
            "result": False, "num": 23,
        }, {
            "result": False, "num": 9,
        }, {
            "result": False, "num": 0,
        }, {
            "result": False, "num": 1.0
        }, {
            "result": False, "num": -9,
        }, {
            "result": False, "num": 'string',
        }, {
            "result": False, "num": '24'
        }, {
            "result": False, "num": [24, 120],
        }, {
            "result": False, "num": {'data': 40320}
        }, {
            "result": False, "num": None
        }]

        for test in tests:
            my_num = test['num']
            expected = test['result']
            result = is_factorial(my_num)
            self.assertEqual(result, expected)

    def test_parse_int(self):
        """
        test ml.misc.interview.parse_int
        @return:
        """
        from ml.misc.interview import parse_int
        tests = [{
            "input": '178',  "result": 178,
        }, {
            "input": '-225', "result": -225,
        }, {
            "input": str(sys.maxsize), "result": sys.maxsize,
        }, {
            "input": str(-sys.maxsize), "result": -sys.maxsize,
        }, {
            "input": str(sys.maxsize+1), "result": sys.maxsize+1,
        }, {
            "input": str(-sys.maxsize-1), "result": -sys.maxsize-1,
        }, {
            "input": '0', "result": 0,
        }, {
            "input": '     199', "result": 199,
        }, {
            "input": '-665     ', "result": -665,
        }, {
            "input": '    1995     \n  ', "result": 1995
        }, {
            "input": 17, "result": 17,
        }, {
            "input": 'string', "result": None,
        }, {
            "input": '-string', "result": None,
        }, {
            "input": '1string5', "result": None,
        }, {
            "input": 'string15', "result": None,
        }, {
            "input": '15string', "result": None,
        }, {
            "input": '      string      15', "result": None,
        }, {
            "input": '1.79', "result": None,
        }, {
            "input": 1.79, "result": None,
        }, {
            "input": ['string', 'list'], "result": None,
        }, {
            "input": {'string': 'string'}, "result": None,
        }, {
            "input": '+', "result": None,
        }, {
            "input": '-', "result": None,
        }, {
            "input": '', "result": None,
        }, {
            "input": '     ', "result": None,
        }, {
            "input": None, "result": None,
        }]

        for test in tests:
            input_item = test["input"]
            expected = test["result"]
            result = parse_int(input_item)
            self.assertEqual(result, expected)
