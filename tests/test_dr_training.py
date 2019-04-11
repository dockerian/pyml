"""
# test_dr_training.py

"""
import logging
import os
import unittest
import numpy

from mock import MagicMock
from mock import patch

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class DrTrainingTests(unittest.TestCase):
    """
    DrTrainingTests includes all unit tests for ml.digit_recognizer.training module
    """
    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.repo_path = os.path.dirname(self.test_path)
        self.proj_path = os.path.join(self.repo_path, "ml")
        self.base_path = os.path.join(self.repo_path, "ml", "digit_recognizer")
        self.data_path = os.path.join(self.repo_path, "ml", "digit_recognizer", "datasets")
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    @patch('ml.digit_recognizer.training.DataSvc')
    @patch('ml.digit_recognizer.training.l_layer_model')
    def test_run(self, mock_func, mock_svc):
        """
        test ml.digit_recognizer.training.run
        @return:
        """
        from ml.digit_recognizer.training import run
        mock_svc.return_value = MagicMock(trainings={'x': numpy.array([[0]]), 'y': numpy.array([[0]])})
        mock_save = MagicMock()
        param = MagicMock(save=mock_save)
        mock_func.return_value = param
        run()
        mock_func.assert_called_once()
        param.save.assert_called_once()
