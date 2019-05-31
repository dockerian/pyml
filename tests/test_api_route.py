"""
# test_api_v1_route.py
"""
import logging
import unittest
import mock

from starlette.datastructures import URL
from starlette.requests import Request
from ml.api.__route import \
    api_icon, \
    api_info, api_root, \
    api_v1_redirect, \
    get_info


class ApiRouteTester(unittest.TestCase):
    """
    ApiRouteTester includes all unit tests for ml.api.__route module
    """

    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        self.mock_scope = {
            "headers": "",
            "path": "",
            "query_string": "",
            "root_path": "",
            "type": "http",
        }
        self.mock_request = Request(scope=self.mock_scope)
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    @mock.patch('ml.api.__route.RedirectResponse')
    def test_api_icon(self, mock_redirect):
        mock_result = 'redirect_api_icon'
        mock_redirect.return_value = mock_result
        result = api_icon()
        mock_redirect.assert_called_with(url='/static/favicon.ico', status_code=302)
        self.assertEqual(result, mock_result)

    @mock.patch('ml.api.__route.RedirectResponse')
    def test_api_info(self, mock_redirect):
        mock_result = 'redirect_api_info'
        mock_redirect.return_value = mock_result
        result = api_info()
        mock_redirect.assert_called_with(url='/api/info', status_code=302)
        self.assertEqual(result, mock_result)

    @mock.patch('ml.api.__route.RedirectResponse')
    def test_api_root(self, mock_redirect):
        mock_result = 'redirect_api_root'
        mock_redirect.return_value = mock_result
        result = api_root()
        mock_redirect.assert_called_with(url='/api/ui', status_code=302)
        self.assertEqual(result, mock_result)

    @mock.patch('ml.api.__route.RedirectResponse')
    def test_api_v1(self, mock_redirect):
        mock_request = self.mock_request
        mock_result = 'root_redirect'
        mock_redirect.return_value = mock_result
        mock_rest_path = 'test?q=1&param=foobar'
        mock_request._url = URL('https://127.0.0.1:8081/api/v1/' + mock_rest_path)
        expected_url = '/api/' + mock_rest_path
        result = api_v1_redirect(mock_request, mock_rest_path)
        mock_redirect.assert_called_with(url=expected_url, status_code=307)
        self.assertEqual(result, mock_result)
        pass

    def test_get_info(self):
        # from mock import MagicMock
        mock_request = self.mock_request
        result = get_info(mock_request)
        self.assertIsNotNone(result)
        self.assertEqual(result['version'], '1.0.0')
