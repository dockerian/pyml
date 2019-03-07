"""
# test_common_parameters.py

"""
import logging
import os
import unittest
import numpy

from mock import MagicMock
from mock import patch

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class DrDataSvcTests(unittest.TestCase):
    """
    DrDataSvcTests includes all unit tests for ml.common.parameters module
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

    @patch('ml.common.parameters.np')
    def test_load(self, mock_np):
        """
        test ml.common.parameters :: Parameters :: load
        """
        from ml.common.parameters import Parameters

        obj = Parameters('does not exist')
        self.assertEqual(obj.base_path, self.base_path)

        obj = Parameters(self.test_path, 'file name')
        self.assertEqual(obj.base_path, self.test_path)

        mock_np_load_result = MagicMock()
        mock_np_load_result.item.return_value = 'np load'
        mock_np.load.return_value = mock_np_load_result

        obj.load()
        param_file = os.path.join(self.test_path, 'datasets', 'file name')
        mock_np.load.assert_called_with(param_file)
        self.assertEqual(obj._parameters, 'np load')
        pass

    @patch('ml.common.parameters.np')
    def test_save(self, mock_np):
        """
        test ml.common.parameters :: Parameters :: save
        """
        from ml.common.parameters import Parameters

        obj = Parameters('does not exist')
        self.assertEqual(obj.base_path, self.base_path)

        obj = Parameters(self.test_path, 'file name')
        self.assertEqual(obj.base_path, self.test_path)

        obj.save('params')
        param_file = os.path.join(self.test_path, 'datasets', 'file name')
        mock_np.save.assert_called_with(param_file, 'params', allow_pickle=True, fix_imports=True)
        pass

    def test_update(self):
        """
        test ml.common.parameters :: Parameters :: update
        :return:
        """
        from ml.common.parameters import Parameters

        obj = Parameters('does not exist')
        self.assertEqual(obj.base_path, self.base_path)

        obj = Parameters(self.test_path, 'file name')
        self.assertEqual(obj.base_path, self.test_path)

        tests = [{
            "grads": {"dW1": numpy.array([[1, 2], [3, 4], [5, 6]]), "db1": numpy.array([[1], [2], [3]])},
            "learning_rate": 1,
            "result": {"W1": numpy.array([[0, 0], [0, 0], [0, 0]]), "b1": numpy.array([[0], [0], [0]])},
        }, {
            "grads": {"dW1": numpy.array([[1, 2], [3, 4], [5, 6]]), "db1": numpy.array([[1], [2], [3]])},
            "learning_rate": 2,
            "result": {"W1": numpy.array([[-1, -2], [-3, -4], [-5, -6]]), "b1": numpy.array([[-1], [-2], [-3]])},
        }]
        for test in tests:
            obj._parameters = {"W1": numpy.array([[1, 2], [3, 4], [5, 6]]), "b1": numpy.array([[1], [2], [3]])}
            grads = test["grads"]
            learning_rate = test["learning_rate"]
            expected = test["result"]
            obj.update(grads, learning_rate)
            self.assertListEqual(obj._parameters["W1"].tolist(), expected["W1"].tolist())
            self.assertListEqual(obj._parameters["b1"].tolist(), expected["b1"].tolist())

    def test_initialize_parameters_deep_he(self):
        """
        test ml.common.parameters :: Parameters :: initialize_parameters_deep_he
        :return:
        """
        from ml.common.parameters import Parameters

        obj = Parameters('does not exist')
        self.assertEqual(obj.base_path, self.base_path)

        obj = Parameters(self.test_path, 'file name')
        self.assertEqual(obj.base_path, self.test_path)

        tests = [{
            "ld": [1, 2, 3],
            "parameters": {
                    "W1": [[2.2971712432704137], [-0.8651542170526618]],
                    "b1": [[0.], [0.]],
                    "W2": [[-0.5281717522634557, -1.0729686221561705],
                           [0.8654076293246785, -2.3015386968802827],
                           [1.74481176421648, -0.7612069008951028]],
                    "b2": [[0.], [0.], [0.]]},
        }]
        for test in tests:
            layer_dims = test["ld"]
            expected_parameters = test["parameters"]
            obj.initialize_parameters_deep_he(layer_dims)
            for i in range(2):
                obj._parameters["W" + str(i + 1)] = obj._parameters["W" + str(i + 1)].tolist()
                obj._parameters["b" + str(i + 1)] = obj._parameters["b" + str(i + 1)].tolist()
            self.assertDictEqual(obj._parameters, expected_parameters)
