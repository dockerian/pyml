"""
# test_api_v1
"""
import logging
import unittest
import mock

from ml.api_v1 import getInfo
from ml.api_v1 import getApiDoc


class ApiV1InitTester(unittest.TestCase):
    """
    ApiV1InitTester includes all unit tests for ml.app module
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

    @mock.patch('ml.api_v1.info')
    def test_info_functions(self, mock_info):
        getInfo()
        mock_info.get_info.assert_called()
        getApiDoc()
        mock_info.get_api_doc.assert_called()
        pass
