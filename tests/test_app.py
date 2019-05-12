"""
# test_app
"""
import logging
import unittest

from mock import patch
from ml.app import main, root


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

    @patch('ml.app.app')
    def test_main(self, mock_app):
        main()
        mock_app.add_api.assert_called()
        mock_app.run.assert_called()

    @patch('ml.app.main')
    def test_main_module(self, mock_main):
        pass

    @patch('ml.app.redirect')
    def test_root(self, mock_redirect):
        mock_result = 'root_redirect'
        mock_redirect.return_value = mock_result
        result = root()
        mock_redirect.assert_called_with('/api/ui', code=302)
        self.assertEqual(result, mock_result)
        pass
