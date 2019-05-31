"""
# test_app_fastapi
"""
import logging
import unittest

from mock import patch
from ml.app_config import api_name, api_desc


class AppFastApiTester(unittest.TestCase):
    """
    AppFastApiTester includes all unit tests for ml.app_fastapi module
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

    @patch('ml.app_fastapi.fastapi')
    @patch('ml.app_fastapi.router_info')
    def test_api(self, mock_router, mock_fastapi):
        from ml.app_fastapi import app
        self.assertIsNotNone(app)
        self.assertEqual(app.title, api_name)
        self.assertEqual(app.description, api_desc)
        self.assertEqual(app.version, '1.0.0')
        pass
