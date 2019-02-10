"""
# test_common_parameters.py

"""
import logging
import os
import unittest

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
        test ml.common.parameters :: Parameters :: load
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
