"""
logger module

@author: Jason Zhu
@email: jason_zhuyx@hotmail.com
"""

import os
import logging
import logging.config
import yaml

__80DOTS__ = ''*80
__CONFIG__ = None  # initialized as None
__YFNAME__ = 'logging.yaml'


def get_logger(name, level=logging.INFO):
    """
    Get a logger and load logging.yaml config file if exists.
    """
    # Set a basic level of logging
    logging.basicConfig(level=logging.INFO)

    load_logging_config()  # loading logging config if not loaded yet

    # print('setting logger[{}] level:{}'.format(name, level))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def load_logging_config():
    """
    Load logging configuration.
    """
    global __CONFIG__

    if __CONFIG__:
        logging.config.dictConfig(__CONFIG__)
        return  # logging config has already been loaded

    # Get the path to the logging config yaml
    dir_py_file = os.path.dirname(os.path.realpath(__file__))
    dir_project = os.path.dirname(dir_py_file)
    yml_logging = os.path.join(dir_project, __YFNAME__)

    # Load up the logger based on the configs
    # print('checking "{}" ...'.format(yml_logging))
    if os.path.exists(yml_logging):
        with open(yml_logging, 'r') as file_stream:
            config = yaml.load(file_stream.read())
            logging.config.dictConfig(config)
            print_logging_config(config)
            __CONFIG__ = config


def print_logging_config(config):
    """
    Print logging config.
    """
    print(__80DOTS__)
    print('-- {}: {}\n'.format(__YFNAME__, config))
    # import json
    # print(__80DOTS__)
    # print('-- {}:\n{}\n'.format(
    #     __YFNAME__, json.dumps(config, sort_keys=True, indent=2)))
    # print(__80DOTS__)
    pass


def print_info():
    """
    Print system and environment info.
    """
    import sys
    print('System version:', sys.version.replace('\n', ' '))
    print_pypath()


def print_pypath():
    """
    Print out Python path.
    """
    import sys
    print('System version:', sys.version.replace('\n', ' '))
    print('\nPYTHONPATH\n{}'.format(__80DOTS__))
    for pylib_path in sys.path:
        print(pylib_path)
    print(__80DOTS__)
    pass


def raise_ni(method_name):
    """
    Raise NotImplementedError on specified method name
    """
    raise NotImplementedError(
        'must implement {} in derived class'.format(method_name))
