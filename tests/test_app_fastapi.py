"""
# test_app_fastapi
"""
import logging
import unittest

from starlette.requests import Request
from ml.app_fastapi import getInfo


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

    def test_getInfo(self):
        # from mock import MagicMock
        scope = {
            "headers": "",
            "path": "",
            "query_string": "",
            "root_path": "",
            "type": "http",
        }
        request = Request(scope=scope)
        result = getInfo(request)
        self.assertIsNotNone(result)
        self.assertEqual(result['version'], '1.0.0')
