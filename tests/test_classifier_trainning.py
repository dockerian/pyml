"""
# test_classifier_training.py

"""
import logging
import os
import unittest

from mock import MagicMock
from mock import patch

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class ClassifierTrainingTests(unittest.TestCase):
    """
    ClassifierTrainingTests includes all unit tests for ml.classifier.training module
    """
    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.repo_path = os.path.dirname(self.test_path)
        self.proj_path = os.path.join(self.repo_path, "ml")
        self.base_path = os.path.join(self.repo_path, "ml", "classifier")
        self.data_path = os.path.join(self.repo_path, "ml", "classifier", "datasets")
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    @patch('ml.classifier.training.l_layer_model')
    def test_run(self, mock_func):
        """
        test ml.classifier.training.run
        @return:
        """
        from ml.classifier.training import run
        mock_save = MagicMock()
        param = MagicMock(save=mock_save)
        mock_func.return_value = param
        run()
        mock_func.assert_called_once()
        param.save.assert_called_once()
