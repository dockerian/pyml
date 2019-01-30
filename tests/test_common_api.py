"""
test_common_api.py
"""
import unittest

from mock import MagicMock, patch

from ml.common.api import build_api_url
from ml.common.api import build_filter_value
from ml.common.api import get_api_data


class CommonApiTester(unittest.TestCase):

    @classmethod
    def teardown_class(cls):
        pass

    def setUp(self):
        """setup for test"""
        self.api_url = 'https://test.com/api/v1'
        self.headers = {
            "Authorization": "Token token={}".format('authz_token'),
            "Content-Type": "application/json"
        }
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    def test_build_api_url(self):
        tests = [{
            'url': 'a_url', 'func': 'a_func', 'args': {},
            'expected': 'a_url/a_func'
        }, {
            'url': 'a_url', 'func': 'a_func', 'args': {"x": 1, "y": 2},
            'expected': 'a_url/a_func?x=1&y=2'
        }, {
            'url': 'a_url', 'func': None, 'args': {},
            'expected': 'a_url'
        }, {
        }]
        num = 0
        for test in tests:
            test_expected = test.get('expected')
            test_args = test.get('args') or {}
            test_func = test.get('func')
            test_url = test.get('url')
            msg = ('test #%02d: url={}, func={}, args={}, expected={}' % num).format(
                test_url, test_func, test_args, test_expected)
            result = build_api_url(test_url, test_func, **test_args)
            self.assertEqual(result, test_expected, msg)
            num += 1
        pass

    def test_build_filter_value(self):
        tests = [{
            'filters': {"a": 123, "x": "test"},
            'expected': 'a == "123" and x == "test"'
        }, {
            'filters': {"key": "value"},
            'expected': 'key == "value"'
        }, {
            'filters': {},
            'expected': ''
        }, {
        }]
        num = 0
        for test in tests:
            test_expected = test.get('expected') or ''
            test_filters = test.get('filters') or {}
            test_op = test.get('op') or 'and'
            msg = ('test #%02d: op={}, filters={}, expected={}' % num).format(
                test_op, test_filters, test_expected)
            result = build_filter_value(test_filters, test_op)
            self.assertEqual(result, test_expected, msg)
            num += 1
        pass

    @patch('ml.common.api.urllib.request')
    def test_get_api_data(self, mock_request):
        _html = '<html><body></body></html>'
        tests = [{
            'status': 200, 'content': '{"a": 1, "x": 3.14}', 'type': 'application/json',
            'expected': {"a": 1, "x": 3.14}
        }, {
            'status': 200, 'content': '', 'type': 'application/json',
            'expected': Exception(),
        }, {
            'status': 200, 'content': _html,
            'expected': {'data': _html},
        }, {
            'status': 500, 'content': '',
            'expected': None,
        }, {
        }]
        result = None
        num = 0
        for test in tests:
            test_content = test.get('content') or ''
            test_expected = test.get('expected')
            test_status = test.get('status')

            mock_data = MagicMock()
            mock_headers = {'content-type': test.get('type', 'text/html')}
            mock_res = MagicMock(status=test_status, headers=mock_headers)
            mock_res.read.return_value = mock_data
            mock_request.urlopen.return_value.__enter__.return_value = mock_res if test_status else None  # noqa
            mock_data.decode.return_value = test_content
            msg = ('test #%02d: status={}, content={}' % num).format(
                test_status, test_content)
            if isinstance(test_expected, Exception):
                with self.assertRaises(Exception) as ctx:
                    ctx_msg = 'unable to read data from request'
                    result, status = get_api_data(self.api_url, self.headers)
                    self.assertEqual(status, test_status)
                    self.assertTrue(ctx_msg in str(ctx.exception), msg)
                    self.assertEqual(result, None, msg)
                pass
            else:
                result, status = get_api_data(self.api_url, self.headers)
                self.assertEqual(result, test_expected, msg)
                self.assertEqual(status, test_status)
            num += 1
        pass
