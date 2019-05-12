"""
# test_api_v1_info
"""
import os
import logging
import unittest

from mock import patch
from ml.api.v1.info import get_api_doc
from ml.api.v1.info import get_info


class ApiV1InfoTester(unittest.TestCase):
    """
    ApiV1InfoTester includes all unit tests for ml.api.v1.info module
    """

    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        test_path = os.path.dirname(os.path.realpath(__file__))
        proj_path = os.path.dirname(test_path)
        self.spec_path = os.path.join(
            proj_path, 'ml', 'apidoc', 'v1')
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    @patch('ml.api.v1.info.flask')
    def test_get_api_doc(self, mock_flask):
        """
        test ml.api.v1.info.get_api_doc
        """
        get_api_doc()
        mock_flask.send_from_directory.assert_called_with(
            self.spec_path, 'swagger.yaml',
            as_attachment=True,
            attachment_filename='swagger-pyml.yaml',
            mimetype='application/octet-stream'
        )
        pass

    def test_get_info(self):
        """
        test ml.api.v1.info.get_info
        """
        result = get_info()
        self.assertEqual(result.get('name'), 'API Service')
