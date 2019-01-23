"""
# test_config

@author: Jason Zhu
@email: jason_zhuyx@hotmail.com

"""
import logging
import os
import pytest
import unittest

from mock import MagicMock, patch, mock_open

from ml.config import check_encrypted_text
from ml.config import get_boolean
from ml.config import get_config_data
from ml.config import get_integer, get_uint
from ml.config import settings


class ConfigTester(unittest.TestCase):
    """
    ConfigTester includes all unit tests for config module
    """

    @classmethod
    def teardown_class(cls):
        logging.shutdown()

    def setUp(self):
        """setup for test"""
        self.encrypted_text = "AQICAHgBtb0SZhoZJa0NRdEJtBKhwIPnNwIJwKkl1vAEW6J5QQFPeFHeIcodADhZJeXAS+5rAAAAZTBjBgkqhkiG9w0BBwagVjBUAgEAME8GCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQM88RpHZ6PwRlP43jJAgEQgCLzBTGKBxo1bvM02eT0f/wrQVaYhc17zyXjQ2fP6oM7arbG"  # noqa
        self.decrypted_text = "aws kms"
        pass

    def tearDown(self):
        """tearing down at the end of the test"""
        pass

    @unittest.skip("skipping boto3")
    @pytest.mark.skip(reason="not imported boto3 yet")
    @patch('ml.config.boto3')
    def test_check_encrypted_text(self, mock_boto3):
        """
        test ml.config.check_encrypted_text
        """
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        mock_client.decrypt.return_value = {'Plaintext': self.decrypted_text}
        result = check_encrypted_text('password', self.encrypted_text)
        self.assertEqual(result, self.decrypted_text)
        result = check_encrypted_text('username', self.encrypted_text)
        self.assertEqual(result, self.encrypted_text)
        result = check_encrypted_text('some_key', 'some_value')
        self.assertEqual(result, 'some_value')

    @patch('ml.config.settings')
    def test_get_boolean(self, mock_settings):
        """
        test ml.config.get_boolean
        """
        tests = [
            {"key": "", "def": None, "mock": "", "expected": False},
            {"key": "TEST_01", "def": None, "mock": "", "expected": False},
            {"key": "TEST_02", "def": None, "mock": "1", "expected": True},
            {"key": "TEST_03", "def": None, "mock": "11", "expected": False},
            {"key": "TEST_04", "def": None, "mock": "yes", "expected": True},
            {"key": "TEST_05", "def": None, "mock": "Yes", "expected": True},
            {"key": "TEST_06", "def": None, "mock": "on", "expected": True},
            {"key": "TEST_07", "def": None, "mock": "ON", "expected": True},
            {"key": "TEST_08", "def": None, "mock": "true", "expected": True},
            {"key": "TEST_09", "def": None, "mock": "True", "expected": True},
            {"key": "TEST_10", "def": None, "mock": "test", "expected": False},
            {"key": "TEST_11", "def": False, "mock": "yes", "expected": True},
            {"key": "TEST_12", "def": False, "mock": "YES", "expected": True},
            {"key": "TEST_13", "def": False, "mock": "On", "expected": True},
            {"key": "TEST_14", "def": False, "mock": "ON", "expected": True},
            {"key": "TEST_15", "def": False, "mock": "TRUE", "expected": True},
            {"key": "TEST_16", "def": False, "mock": "True", "expected": True},
            {"key": "TEST_17", "def": False, "mock": "1", "expected": True},
            {"key": "TEST_18", "def": False, "mock": "NaN", "expected": False},
            {"key": "TEST_19", "def": True, "mock": "1234567", "expected": False},
            {"key": "TEST_20", "def": True, "mock": "111", "expected": False},
            {"key": "TEST_21", "def": False, "mock": "", "expected": False},
            {"key": "TEST_22", "def": True, "mock": "", "expected": True},
        ]
        for test in tests:
            mock_settings.return_value = test["mock"]
            result = get_boolean(test["key"]) if test["def"] is None else \
                get_boolean(test["key"], test["def"])
            msg = "key: {}, result: {}, expected: {}".format(
                test["key"], result, test["expected"])
            self.assertEqual(result, test["expected"], msg)

    def test_get_config_data(self):
        """
        test ml.config.get_config_data
        """
        config_data = get_config_data()
        self.assertIsInstance(config_data, dict)
        pass

    @patch('ml.config.settings')
    def test_get_integer(self, mock_settings):
        """
        test ml.config.get_integer
        """
        result = get_integer('', 99)
        self.assertEqual(result, 99)

        tests = [
            {"key": "TEST_01", "def": 0, "mock": "", "expected": 0},
            {"key": "TEST_02", "def": 1, "mock": "NaN", "expected": 1},
            {"key": "TEST_03", "def": 123456, "mock": "31415926", "expected": 31415926},
            {"key": "TEST_04", "def": 654321, "mock": "-31415926", "expected": -31415926},
            {"key": "TEST_05", "def": 555, "mock": "-360", "expected": -360},
            {"key": "TEST_06", "def": 0, "mock": "064", "expected": 64},
        ]
        for test in tests:
            mock_settings.return_value = test["mock"]
            result = get_integer(test["key"], test["def"])
            msg = "key: {}, def: {}, result: {}, expected: {}".format(
                test["key"], test["def"], result, test["expected"])
            self.assertEqual(result, test["expected"], msg)

        mock_settings.side_effect = ValueError('x', 'msg')
        result = get_integer('ENV_NAME', 987654321)
        self.assertEqual(result, 987654321)

    @patch('ml.config.settings')
    def test_get_uint(self, mock_settings):
        """
        test ml.config.get_uint
        """
        result = get_uint('', 99)
        self.assertEqual(result, 99)

        tests = [
            {"key": "TEST_01", "def": 0, "mock": "", "expected": 0},
            {"key": "TEST_02", "def": 1, "mock": "NaN", "expected": 1},
            {"key": "TEST_03", "def": 123456, "mock": "31415926", "expected": 31415926},
            {"key": "TEST_04", "def": 654321, "mock": "-31415926", "expected": 654321},
            {"key": "TEST_05", "def": 333, "mock": "abc", "expected": 333},
            {"key": "TEST_06", "def": 0, "mock": "064", "expected": 64},
        ]
        for test in tests:
            mock_settings.return_value = test["mock"]
            result = get_uint(test["key"], test["def"])
            msg = "key: {}, def: {}, result: {}, expected: {}".format(
                test["key"], test["def"], result, test["expected"])
            self.assertEqual(result, test["expected"], msg)

        mock_settings.side_effect = ValueError('x', 'msg')
        result = get_uint('ENV_NAME', 987654321)
        self.assertEqual(result, 987654321)

    def test_settings(self):
        """
        test ml.config.settings
        """
        data = """
        db:
            user: bar
            pass: barcode
        sys:
            users:
                - foo
                - bar
                - test
                - zoo
        """
        tests_path = os.path.dirname(os.path.realpath(__file__))
        upper_path = os.path.dirname(tests_path)
        config_dir = os.path.join(upper_path, "ml", "config.yaml")
        os.environ["DB_PORT"] = "13306"
        # reset Config singleton in order to mock with test data
        from ml.config import Config
        Config.reset()
        with patch('builtins.open', mock_open(read_data=data)) as mock_file:
            allset = settings()
            v_none = settings('this.does.not.exist')
            v_port = settings('db.port')
            v_test = settings('sys.users.2')
            v_user = settings('db.user')
            # in PyCharm, actual open(config_dir, 'a', encoding='utf8')
            mock_file.assert_called_with(config_dir, "rt")
            self.assertEqual(allset['sys.users.0'], 'foo')
            self.assertEqual(v_port, '13306')
            self.assertEqual(v_test, 'test')
            self.assertEqual(v_user, 'bar')
            self.assertEqual(v_none, '')
        # re-initialize Config singleton
        Config.reset()
        config = Config(config_file='NON-EXIST-YAML-FILE')
        self.assertEqual(config.settings, {})
        Config.reset()
