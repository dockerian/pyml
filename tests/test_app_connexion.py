"""
# test_app_connexion
"""
import logging
import unittest

from mock import patch
from ml.app_connexion import \
    app_main, \
    config_connexion, \
    check_cert, \
    https_before_request, \
    root_api_v1, root_api, \
    root_icon, \
    root


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

    @patch('ml.app_connexion.app')
    def test_config_connexion(self, mock_app):
        config_connexion()
        mock_app.add_api.assert_called()

    @patch('ml.app_connexion.app')
    def test_main(self, mock_app):
        app_main()
        mock_app.run.assert_called()

    @patch('ml.app_connexion.app_main')
    def test_main_module(self, mock_main):
        # import runpy
        # runpy.run_module('ml.app', run_name='__main__')
        pass

    @patch('ml.app_connexion.os')
    @patch('ml.app_connexion.app')
    @patch('ml.app_connexion.get_boolean')
    def test_check_cert(self, mock_get, mock_app, mock_os):
        from ml.app_connexion import SSL_CONTEXT
        tests = [{
            "ssl": False, "mock_isfile": False,
        }, {
            "ssl": False, "mock_isfile": True,
        }, {
            "ssl": True, "mock_isfile": False,
        }, {
            "ssl": True, "mock_isfile": True,
        }]
        for test in tests:
            ssl_enabled = test.get('ssl')
            no_cert = not test.get('mock_isfile') and SSL_CONTEXT is None
            mock_get.return_value = ssl_enabled
            mock_os.path.isfile.return_value = test.get('mock_isfile')
            result = check_cert()
            if ssl_enabled and SSL_CONTEXT:
                mock_app.app.before_request.assert_called()
            self.assertEqual(result is None, no_cert or not ssl_enabled)

    @patch('ml.app_connexion.request')
    @patch('ml.app_connexion.redirect')
    def test_https_before_request(self, mock_redirect, mock_request):
        expected = 'https://host:8080/api/route'
        mock_request.url = 'http://host:8080/api/route'
        https_before_request()
        mock_redirect.assert_called_with(expected, code=301)

    @patch('ml.app_connexion.redirect')
    def test_root_api(self, mock_redirect):
        mock_result = 'root_redirect'
        mock_redirect.return_value = mock_result
        result = root_api()
        mock_redirect.assert_called_with('/api/info', code=302)
        self.assertEqual(result, mock_result)
        pass

    @patch('ml.app_connexion.request')
    @patch('ml.app_connexion.redirect')
    def test_root_api_v1(self, mock_redirect, mock_request):
        mock_result = 'root_redirect'
        mock_redirect.return_value = mock_result
        mock_rest_path = 'test?q=1&param=foobar'
        mock_request.host_url = 'https://127.0.0.1:8081/'
        mock_request.url = 'https://127.0.0.1:8081/api/v1/' + mock_rest_path
        expected_url = '/api/' + mock_rest_path
        result = root_api_v1(mock_rest_path)
        mock_redirect.assert_called_with(expected_url, code=307)
        self.assertEqual(result, mock_result)
        pass

    @patch('ml.app_connexion.redirect')
    def test_root_icon(self, mock_redirect):
        mock_result = 'root_redirect_static_api_png'
        mock_redirect.return_value = mock_result
        result = root_icon()
        mock_redirect.assert_called_with('/static/api.png', code=302)
        self.assertEqual(result, mock_result)
        pass

    @patch('ml.app_connexion.redirect')
    def test_root(self, mock_redirect):
        mock_result = 'root_redirect'
        mock_redirect.return_value = mock_result
        result = root()
        mock_redirect.assert_called_with('/api/ui', code=302)
        self.assertEqual(result, mock_result)
        pass
