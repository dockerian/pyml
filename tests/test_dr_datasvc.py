"""
# test_classifier_datasvc.py.py

"""
import logging
import os
import unittest
import numpy

from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


class DrDataSvcTests(unittest.TestCase):
    """
    DrDataSvcTests includes all unit tests for ml.digit_recognizer.datasvc module
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

    def test_load(self):
        """
        test ml.digit_recognizer.data_svc :: DataSvc :: load
        """
        from ml.digit_recognizer.datasvc import DataSvc

        svc = DataSvc('does not exist')
        self.assertEqual(svc.base_path, self.base_path)

        svc = DataSvc(self.test_path)
        self.assertEqual(svc.base_path, self.test_path)

        svc.load('mini_train')
        x_training = svc.trainings['x']
        y_training = svc.trainings['y']
        self.assertIsInstance(x_training, numpy.ndarray)
        self.assertIsInstance(y_training, numpy.ndarray)

        x_testing = svc.trainings['x']
        y_testing = svc.trainings['y']
        self.assertIsInstance(x_testing, numpy.ndarray)
        self.assertIsInstance(y_testing, numpy.ndarray)
        pass
