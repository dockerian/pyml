"""
# test_classifier_datasvc.py.py

"""
import logging
import os
import unittest
import numpy

from ml.common.mathEx import \
    change_to_multi_class, \
    compute_cost, \
    compute_cost_with_l2_regularization, \
    leaky_relu, \
    leaky_relu_backward, \
    l_model_forward, \
    l_model_backward_with_l2, \
    one_vs_all_prediction, \
    relu, \
    relu_backward, \
    sigmoid, \
    sigmoid_backward
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class MathExTests(unittest.TestCase):
    """
    mathExTests includes all unit tests for ml.common.mathEx module
    """
    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.repo_path = os.path.dirname(self.test_path)
        self.proj_path = os.path.join(self.repo_path, "ml")
        self.base_path = os.path.join(self.repo_path, "ml", "common")
        self.data_path = os.path.join(self.repo_path, "ml", "common", "datasets")
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test_change_to_multi_class(self):
        """
        test ml.common.mathEx.change_to_multi_class
        @return:
        """
        tests = [
            {"y": [[0, 1, 2]], "result": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
            {"y": [[0, 3]], "result": [[1, 0], [0, 0], [0, 0], [0, 1]]},
            {"y": [[0]], "result": [[1]]},
            {"y": [[0.5]], "result": [[1]]},
            {"y": None, "result": [[1]]},
        ]

        for test in tests:
            y = test["y"]
            expected = test['result']
            result = change_to_multi_class(numpy.array(y))
            self.assertListEqual(result.tolist(), expected)

    def test_compute_cost(self):
        """
        test ml.common.mathEx.compute_cost
        @return:
        """
        tests = [{
            "al": [[0.5]], "y": [[0.6]],
            "result": [[0.6931471805599453]],
        }, {
            "al": [[0.01, 0.1, 0.2, 0.3], [0.1, 0.2, 0.3, 0.4]],
            "y": [[0.2, 0.3, 0.4, 0.5], [0.3, 0.4, 0.5, 0.6]],
            "result": [[3.2688439245595067]],
        }, {
            "al": None,
            "y": None,
            "result": [[0.6931471805599453]],
        }]

        for test in tests:
            al = test["al"]
            y = test["y"]
            expected = test['result']
            result = compute_cost(numpy.array(al), numpy.array(y))
            self.assertTrue(numpy.abs(expected - result) <= 0.000001)
        al = 0.5
        y = 0.6
        expected = [[0.6931471805599453]]
        result = compute_cost(al, y)
        self.assertTrue(numpy.abs(expected - result) <= 0.000001)

    def test_compute_cost_with_l2_regularization(self):
        """
        test ml.common.mathEx.compute_cost_with_l2_regularization
        @return:
        """
        tests = [{
            "al": [[0.01, 0.1, 0.2, 0.3], [0.1, 0.2, 0.3, 0.4]],
            "y": [[0.2, 0.3, 0.4, 0.5], [0.3, 0.4, 0.5, 0.6]],
            "parameters": {"W1": 1, "W2": 2, "W3": 3, "W4": 4},
            "lambd": 0.075,
            "result": 3.3157189245595067,
        }, {
            "al": [[0.5]],
            "y": [[0.6]],
            "parameters": {"W1": 1, "W2": 2, "W3": 3, "W4": 4},
            "lambd": 0.075,
            "result": 0.8806471805599453,
        }, {
            "al": None,
            "y": None,
            "parameters": {"W1": 1, "W2": 2, "W3": 3, "W4": 4},
            "lambd": 0.075,
            "result": 0.8806471805599453,
        }]

        for test in tests:
            al = test["al"]
            y = test["y"]
            parameters = test["parameters"]
            lambd = test["lambd"]
            expected = test["result"]
            result = compute_cost_with_l2_regularization(numpy.array(al), numpy.array(y), parameters, lambd)
            self.assertTrue(numpy.abs(expected - result) <= 0.000001)
        al = 0.5
        y = 0.6
        parameters = {"W1": 1, "W2": 2, "W3": 3, "W4": 4}
        broken_parameters = {"S1": 1, "b1": 0}
        lambd = 0.075
        expected = [[0.8806471805599453]]
        result = compute_cost_with_l2_regularization(al, y, parameters, lambd)
        self.assertTrue(numpy.abs(expected - result) <= 0.000001)

        with self.assertRaises(KeyError):
            compute_cost_with_l2_regularization(al, y, broken_parameters, lambd)

    def test_relu(self):
        """
        test ml.common.mathEx.relu
        @return:
        """
        tests = [{
            "z": [[1], [-1], [2], [-2]],
            "result_a": [[1], [0], [2], [0]],
            "result_cache": [[1], [-1], [2], [-2]],
        }, {
            "z": [[-1]],
            "result_a": [[0]],
            "result_cache": [[-1]],
        }]
        for test in tests:
            z = test["z"]
            expected_a = test["result_a"]
            expected_cache = test["result_cache"]
            a, cache = relu(numpy.array(z))
            self.assertListEqual(a.tolist(), expected_a)
            self.assertListEqual(cache.tolist(), expected_cache)

        tests_ints = [{
            "z": 1,
            "result_a": [[1]],
            "result_cache": [[1]],
        }, {
            "z": -1,
            "result_a": [[0]],
            "result_cache": [[-1]],
        }]
        for test in tests_ints:
            z = test["z"]
            expected_a = test["result_a"]
            expected_cache = test["result_cache"]
            a, cache = relu(z)
            self.assertListEqual(a.tolist(), expected_a)
            self.assertListEqual(cache.tolist(), expected_cache)

    def test_relu_backward(self):
        """
        test ml.common.mathEx.relu_backward
        @return:
        """
        tests = [{
            "da": [[1], [2], [3], [4]],
            "cache": [[1], [0], [1], [0]],
            "result": [[1], [0], [3], [0]],
        }, {
            "da": [[1]],
            "cache": [[-1]],
            "result": [[0]],
        }, {
            "da": [[1]],
            "cache": [[0]],
            "result": [[0]],
        }]
        for test in tests:
            da = test["da"]
            cache = test["cache"]
            expected = test["result"]
            test = relu_backward(numpy.array(da), numpy.array(cache))
            self.assertListEqual(test.tolist(), expected)

    def test_leaky_relu(self):
        """
        test ml.common.mathEx.leaky_relu
        @return:
        """
        tests = [{
            "z": [[-1], [0], [1], [2]],
            "a": [[-0.01], [0], [1], [2]],
            "cache": [[-1], [0], [1], [2]],
        }, {
            "z": [[-1, 0, 1, 2]],
            "a": [[-0.01, 0, 1, 2]],
            "cache": [[-1, 0, 1, 2]],
        }, {
            "z": [[-2]],
            "a": [[-0.02]],
            "cache": [[-2]],
        }, {
            "z": [[2]],
            "a": [[2]],
            "cache": [[2]],
        }]
        for test in tests:
            z = test["z"]
            expected_a = test["a"]
            expected_cache = test["cache"]
            a, cache = leaky_relu(numpy.array(z))
            self.assertListEqual(a.tolist(), expected_a)
            self.assertListEqual(cache.tolist(), expected_cache)

        z = -1
        expected_a = [[-0.01]]
        expected_cache = [[-1]]
        a, cache = leaky_relu(z)
        self.assertListEqual(a.tolist(), expected_a)
        self.assertListEqual(cache.tolist(), expected_cache)

    def test_leaky_relu_backward(self):
        """
        test ml.common.mathEx.leaky_relu_backward
        @return:
        """
        tests = [{
            "da": [[1], [2], [3], [4]],
            "cache": [[1], [-1], [1], [0]],
            "result": [[1], [0], [3], [0]],
        }, {
            "da": [[1]],
            "cache": [[-1]],
            "result": [[0]],
        }, {
            "da": [[1]],
            "cache": [[0]],
            "result": [[0]],
        }]
        for test in tests:
            da = test["da"]
            cache = test["cache"]
            expected = test["result"]
            test = leaky_relu_backward(numpy.array(da), numpy.array(cache))
            self.assertListEqual(test.tolist(), expected)

    def test_sigmoid(self):
        """
        test ml.common.mathEx.sigmoid
        @return:
        """
        tests_array = [{
            "z": [[0]],
            "a": [[0.5]],
            "cache": [[0]],
        }, {
            "z": [[0.01]],
            "a": [[0.5024999791668749]],
            "cache": [[0.01]],
        }, {
            "z": [[0.5], [0.6]],
            "a": [[0.6224593312018546], [0.6456563062257954]],
            "cache": [[0.5], [0.6]],
        }, {
            "z": [[0.5, 0.6]],
            "a": [[0.6224593312018546, 0.6456563062257954]],
            "cache": [[0.5, 0.6]],
        }]

        for test in tests_array:
            z = test["z"]
            expected_a = test["a"]
            expected_cache = test["cache"]
            a, cache = sigmoid(numpy.array(z))
            self.assertListEqual(a.tolist(), expected_a)
            self.assertListEqual(cache.tolist(), expected_cache)

        tests_int = [{
            "z": 0,
            "a": 0.5,
            "cache": 0,
        }, {
            "z": 0.01,
            "a": 0.5024999791668749,
            "cache": 0.01,
        }]

        for test in tests_int:
            z = test["z"]
            expected_a = test["a"]
            expected_cache = test["cache"]
            a, cache = sigmoid(z)
            self.assertEqual(a, expected_a)
            self.assertEqual(cache, expected_cache)

    def test_sigmoid_backward(self):
        """
        test ml.common.mathEx.sigmoid_backward
        @return:
        """
        tests_array = [{
            "da": [[0.5]],
            "cache": [[0]],
            "result": [[0.125]],
        }, {
            "da": [[-0.5, 0.75]],
            "cache": [[0, 0.5]],
            "result": [[-0.125,  0.17625278415119588]],
        }, {
            "da": [[-0.5], [0.75]],
            "cache": [[0], [0.5]],
            "result": [[-0.125], [0.17625278415119588]],
        }]

        for test in tests_array:
            da = test["da"]
            cache = test["cache"]
            expected = test["result"]
            result = sigmoid_backward(numpy.array(da), numpy.array(cache))
            self.assertListEqual(result.tolist(), expected)

        tests_number = [{
            "da": 0.5,
            "cache": 0,
            "result": [[0.125]],
        }, {
            "da": -0.5,
            "cache": 0,
            "result": [[-0.125]],
        }, {
            "da": 0.75,
            "cache": 0.5,
            "result": [[0.17625278415119588]],
        }]

        for test in tests_number:
            da = test["da"]
            cache = test["cache"]
            expected = test["result"]
            result = sigmoid_backward(da, cache)
            self.assertListEqual(result.tolist(), expected)

    def test_l_model_forward(self):
        """
        test ml.common.l_model_forward
        @return:
        """
        tests = [{
            "x": numpy.array([[1, 2], [3, 4]]),
            "parameters": {
                "W1": numpy.array([[0, 0], [0, 0]]),
                "b1": numpy.array([[0], [0]]),
                "W2": numpy.array([[0, 0], [0, 0]]),
                "b2": numpy.array([[0], [0]])},
            "al": numpy.array([[0.5, 0.5], [0.5, 0.5]]),
            "caches": [
                (
                    (numpy.array([[1, 2], [3, 4]]),
                     numpy.array([[0, 0], [0, 0]]),
                     numpy.array([[0], [0]])),
                    numpy.array([[0, 0], [0, 0]]),
                 ), ((numpy.array([[0., 0.], [0., 0.]]),
                      numpy.array([[0, 0], [0, 0]]),
                      numpy.array([[0], [0]])),
                     numpy.array([[0., 0.], [0., 0.]]))],
        }]
        for test in tests:
            x = test["x"]
            parameters = test["parameters"]
            expected_al = test["al"]
            al, caches = l_model_forward(x, parameters)
            self.assertListEqual(al.tolist(), expected_al.tolist())

    def test_l_model_backward_with_l2(self):
        """
        test ml.common.mathEx.l_model_backward_with_l2
        @return:
        """
        tests = [{
            "al": numpy.array([[0.5, 0.5], [0.5, 0.5]]),
            "y": numpy.array([[0, 0], [0, 0]]),
            "caches": [((numpy.array([[1, 2], [3, 4]]),
                         numpy.array([[0, 0], [0, 0]]),
                         numpy.array([[0], [0]])),
                        numpy.array([[0, 0], [0, 0]])),
                       ((numpy.array([[0., 0.], [0., 0.]]),
                         numpy.array([[0, 0], [0, 0]]),
                         numpy.array([[0], [0]])),
                        numpy.array([[0., 0.], [0., 0.]]))],
            "lambd": 0.075,
            "result": {"dA1": numpy.array([[0., 0.], [0., 0.]]),
                       "dW2": numpy.array([[0., 0.], [0., 0.]]),
                       "db2": numpy.array([[0.5], [0.5]]),
                       "dA0": numpy.array([[0., 0.], [0., 0.]]),
                       "dW1": numpy.array([[0., 0.], [0., 0.]]),
                       "db1": numpy.array([[0.], [0.]])},
        }]
        for test in tests:
            al = test["al"]
            y = test["y"]
            caches = test["caches"]
            lambd = test["lambd"]
            expected = test["result"]
            result = l_model_backward_with_l2(al, y, caches, lambd)
            for i in range(2):
                expected["dA" + str(i)] = expected["dA" + str(i)].tolist()
                expected["dW" + str(i + 1)] = expected["dW" + str(i + 1)].tolist()
                expected["db" + str(i + 1)] = expected["db" + str(i + 1)].tolist()
                result["dA" + str(i)] = result["dA" + str(i)].tolist()
                result["dW" + str(i + 1)] = result["dW" + str(i + 1)].tolist()
                result["db" + str(i + 1)] = result["db" + str(i + 1)].tolist()
            self.assertDictEqual(result, expected)

    def test_one_vs_all_prediction(self):
        """
        test ml.common.mathEx.one_vs_all_prediction
        @return:
        """
        tests = [{
            "pm": [[0], [0.1], [0.2]],
            "result": [[2]],
            }, {
            "pm": [[0, 1, 2], [0.1, 0.2, 0.3], [0.3, 0.2, 0.1]],
            "result": [[2, 0, 0]],
        }]
        for test in tests:
            prob_matrix = test["pm"]
            expected = test["result"]
            result = one_vs_all_prediction(numpy.array(prob_matrix))
            self.assertListEqual(result.tolist(), expected)
