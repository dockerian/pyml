"""
# config

@author: Jason Zhu
@email: jason_zhuyx@hotmail.com

"""
import os
import yaml

from ml.utils.extension import get_json
from ml.utils.logger import get_logger

CONFIG_DEFAULT = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'config.yaml')
LOGGER = get_logger(__name__)


class _Singleton(type):  # pylint: disable=too-few-public-methods
    """
    A metaclass that creates a Singleton base class when called.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        overriding __call__
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(
                _Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset(cls):
        """
        tear down class instances
        """
        cls._instances = {}


class Singleton(_Singleton('SingletonMeta', (object,), {})):  # pylint: disable=too-few-public-methods
    """
    Singleton class
    """
    def __init__(self):
        """
        Singleton class constructor
        """
        # print('- ::constructor::', __class__.__name__)
        pass  # pylint: disable=unnecessary-pass


class Config(Singleton):  # pylint: disable=too-few-public-methods
    """
    Config class derived from Singleton
    """
    def __init__(self, config_file=CONFIG_DEFAULT):
        super(Config, self).__init__()

        self.config_file = config_file
        if not os.path.isfile(self.config_file):
            self.settings = {}
            return

        with open(self.config_file, "rt") as conf:
            LOGGER.info("reading %s", self.config_file)
            self.__data__ = yaml.safe_load(conf)
            LOGGER.info('config data: \n%s', get_json(self.__data__))
            self.settings = flatten_object(self.__data__)
            LOGGER.info('settings: \n%s', get_json(self.settings))


def check_encrypted_text(setting_key, key_val):
    """
    Check if the text is encrypted by a KMS key.
    Notes:
        * Pre-requisites: `boto3`
        * Check `token`, `password` or `key` (case-insensitive) only.
        * Decryption requires an AWS account either in a role based security
          context, or by env/profile settings, e.g.
          - AWS_ACCESS_KEY_ID
          - AWS_SECRET_ACCESS_KEY
          - AWS_DEFAULT_REGION
    """
    text = str(key_val)
    skey = str(setting_key).lower()
    aorp = 'token' in skey or 'password' in skey or 'key' in skey
    if aorp and len(text) > 128 and ' ' not in text:
        # import boto3  # moving to global when this code is uncommented
        # decrypted = boto3.client('kms').decrypt(
        #     CiphertextBlob=b64decode(text))
        # # LOGGER.debug('- decrypted: %s', decrypted)
        # decrypted_text = str(decrypted['Plaintext'], 'utf-8')
        # # LOGGER.debug('- decrypted text: %s', decrypted_text)
        # return decrypted_text
        return text
    return key_val


def flatten_object(obj, result=None):
    """
    Convert a JSON object to a flatten dictionary.

    example: { "db": { "user": "bar" }} becomes {"db.user": "bar" }
    """
    if not result:
        result = {}

    def _flatten(key_obj, name=''):
        if isinstance(key_obj, dict):
            for item in key_obj:
                arg = str(name) + str(item) + '.'
                _flatten(key_obj[item], arg)
        elif isinstance(key_obj, list):
            index = 0
            for item in key_obj:
                arg = str(name) + str(index) + '.'
                _flatten(item, arg)
                index += 1
        else:
            result[name[:-1]] = key_obj

    _flatten(obj)
    return result


def get_boolean(key_name, default_value=False):
    """
    Get boolean value for a key; otherwise, return default value.
    """
    if not key_name:
        return default_value

    key_val = str(settings(str(key_name))).lower()
    if key_val in ["1", "on", "true", "yes"]:
        return True
    return False if key_val else default_value


def get_config_data():
    """
    Get config data object.
    """
    return Config().__data__


def get_integer(key_name, default_value=0):
    """
    Get integer value for a key; otherwise, return default value.
    """
    if not key_name:
        return default_value
    try:
        return int(str(settings(str(key_name))))
    except ValueError:
        return default_value


def get_uint(key_name, default_value=0):
    """
    Get unsigned integer value for a key; otherwise, return default value.
    """
    if not key_name:
        return default_value
    try:
        key_val = str(settings(str(key_name)))
        key_int = int(key_val) if key_val.isdigit() else default_value
        return key_int
    except ValueError:
        return default_value


def settings(setting_key=None, default_value=''):
    """
    Get the instance by a key in application settings (config.yaml file)

    example: print(setttings('mysql.database'))
    """
    config = Config().settings

    if not setting_key:
        return config

    env_var = str.replace(setting_key, ".", "_").upper()
    key_val = os.environ.get(env_var, '')

    if not key_val:
        key_val = config.get(setting_key, default_value)

    # key_val = check_encrypted_text(setting_key, key_val)

    return '' if key_val is None else key_val
