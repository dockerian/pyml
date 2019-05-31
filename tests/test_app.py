"""
# test_app
"""
import logging
import unittest

from mock import patch
from ml.app import application


class AppTester(unittest.TestCase):
    """
    AppTester includes all unit tests for ml.app module
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

    def test_app(self):
        self.assertIsNotNone(application)
        pass

    @patch('ml.app_connexion.app_main')
    def test_main(self, mock_app_main):
        pass
