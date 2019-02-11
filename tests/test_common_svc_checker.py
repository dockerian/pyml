"""
test_common_svc_checker.py
"""
import json
import os
import pytest
import unittest

from mock import patch

from ml.common.svc_checker import ServiceChecker
from ml.utils.logger import get_logger

LOGGER = get_logger('ml.' + __name__)


class ServiceCheckerTester(unittest.TestCase):

    @classmethod
    def teardown_class(cls):
        pass

    def setUp(self):
        """setup for test"""
        self.test_path = os.path.dirname(os.path.realpath(__file__))
        self.repo_path = os.path.dirname(self.test_path)
        self.proj_path = os.path.join(self.repo_path, 'ml')
        self.data_path = os.path.join(self.test_path, 'data')
        self.data_file = os.path.join(self.data_path, 'test_endpoints.json')
        self.data_file_failure = os.path.join(self.data_path, 'test_endpoints_failure_500.json')
        self.data_file_success = os.path.join(self.data_path, 'test_endpoints_success.json')
        self.test_data = {}
        if os.path.isfile(self.data_file):
            with open(self.data_file, 'rt') as fh:
                content = fh.read()
                # LOGGER.debug('\n- Loaded endpoints:\n%s', content)
                self.test_data = json.loads(content)
        self.test_data_success = {}
        if os.path.isfile(self.data_file_success):
            with open(self.data_file_success, 'rt') as fh:
                content = fh.read()
                # LOGGER.debug('\n- Loaded success test data:\n%s', content)
                self.test_data_success = json.loads(content)
        self.test_data_failure = {}
        if os.path.isfile(self.data_file_failure):
            with open(self.data_file_failure, 'rt') as fh:
                content = fh.read()
                # LOGGER.debug('\n- Loaded failure test data:\n%s', content)
                self.test_data_failure = json.loads(content)
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    @patch('ml.common.svc_checker.urlparse')
    def test_check_endpoint_parse(self, mock_urlparse):
        result = None
        mock_urlparse.side_effect = ValueError('value error')
        try:
            svc = ServiceChecker([])
            result = svc._check_endpoint_parse('test')
        except Exception as ex:
            self.assertIsInstance(ex, ValueError)
        self.assertFalse(result)

    @patch('ml.common.svc_checker.get_api_data')
    def test_start(self, mock_get_api_data):
        _res_test = [{
          "name": "endpoint 0-no-response",
          "path": "https://abc/v0/",
        }]
        _res_data = {
          "failure": [
            {
              "_err": "no response data from URL: https://abc/v0",
              "name": "endpoint 0-no-response",
              "path": "https://abc/v0"
            }
          ],
          "success": []
        }
        _top_test = [{
          "name": "endpoint 0-html",
          "desc": "app endpoint v0.",
          "path": "https://abc/v0/",
          "regx": "KIDDING ME",
          "format": "html",
        }, {
          "name": "endpoint 1-check-keys",
          "desc": "application foobar v1.",
          "path": "http://foobar/v1",
          "keys": "do_not_exist",
        }, {
          "name": "endpoint 2-html",
          "desc": "app endpoint v2.",
          "path": "https://xyz/v2/",
          "regx": "<version>",
          "format": "html",
        }, {
          "name": "endpoint 3-bad-url",
          "desc": "bad application foobar v3.",
          "path": "bad/foobar/v3",
        }]
        _top_data = {
          "failure": [
            {
              "_err": "cannot find `KIDDING ME` in response data from: https://abc/v0",
              "name": "endpoint 0-html",
              "path": "https://abc/v0"
            },
            {
              "_err": "missing value by key `do_not_exist` in response data from: http://foobar/v1",
              "name": "endpoint 1-check-keys",
              "path": "http://foobar/v1"
            },
            {
              "_err": "invalid endpoint URL: bad/foobar/v3",
              "base": "",
              "name": "endpoint 3-bad-url",
              "path": "bad/foobar/v3"
            }
          ],
          "success": [{
            "name": "endpoint 2-html",
            "path": "https://xyz/v2"
          }]
        }

        mock_data = {
            "dbInfo": {"name": "dbName"},
            "version": "<version>",
            "test": "test",
        }
        tests = [{
            'status': 200, 'max_level': 0, 'mock_res': mock_data,
            'endpoints': _top_test,
            'expected': _top_data,
        }, {
            'status': 200, 'max_level': 0, 'mock_res': None,
            'endpoints': _res_test,
            'expected': _res_data,
        }, {
            'status': 200, 'max_level': 3, 'mock_res': mock_data,
            'expected': self.test_data_success,
        }, {
            'status': 500, 'max_level': 2, 'mock_res': mock_data,
            'expected': self.test_data_failure,
        }]
        num = 0
        for test in tests:
            status = test.get('status', 200)
            expected = test.get('expected', None)
            endpoints = test.get('endpoints', self.test_data)
            max_level = test.get('max_level', 3)
            mock_res_data = test.get('mock_res', mock_data)
            mock_get_api_data.return_value = (mock_res_data, status)

            checker = ServiceChecker(self.test_data, max_level=max_level)

            for mt in [False, True]:
                checker.start(endpoints, multi_threads=mt)
                results = checker._results
                results_string = json.dumps(results, sort_keys=True, indent=2)
                str1 = 'ServiceChecker results [multi_threads={}]:\n{}'.format(
                    mt, results_string)
                str2 = json.dumps(expected, sort_keys=True, indent=2)
                _msg = 'Test #{}: {}\n{}'.format('%02d' % num, str1, str2)

                for key in ['failure', 'success']:
                    self.assertCountEqual(
                        results[key], expected[key], _msg)
            num += 1
        pass

    @pytest.mark.functest
    def test_start_functest(self):
        """
        functional testing ml.common.svc_checker :: ServiceChecker :: start
        """
        test_data = []
        test_file = os.path.join(self.data_path, 'functest_endpoints.json')
        if os.path.isfile(test_file):
            with open(test_file, 'rt') as fh:
                content = fh.read()
                # LOGGER.debug('\n- Loaded endpoints:\n%s', content)
                test_data = json.loads(content)

        svc = ServiceChecker(test_data)
        expected = []
        for endpoint in test_data:
            data = svc._copy_endpoint(endpoint)
            expected.append(data)

        svc.start(test_data)
        results = svc._results
        self.assertEqual(results['failure'], [], 'should not have failure')
        self.assertCountEqual(results['success'], expected)
        e1 = svc._elapsed

        svc.start(test_data, multi_threads=True)
        results = svc._results
        self.assertEqual(results['failure'], [], 'should not have failure')
        self.assertCountEqual(results['success'], expected)
        e2 = svc._elapsed
        self.assertLess(e2, e1, 'should take less time')
        pass
