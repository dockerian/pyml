"""
# setup module
"""
import os

from setuptools import setup, find_packages

NAME = 'ml'

AUTHOR = 'Jason Zhu'
AUTHOR_EMAIL = 'jason_zhuyx@hotmail.com'
BULD_VERSION = '1.0.0'  # in format of `<major>.<minor>.<release>`
PROJECT_CODE_NAME = 'Moonlight'
PROJECT_DESCRIPTION = 'Python Machine Learning Practice'
PROJECT_URL = ''
SUBJECT = 'Machine Learning'

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as f:
    README = f.read()

# use project folder as BASE
BASE = NAME if os.path.isdir(os.path.join(HERE, NAME)) else HERE

# assume `requirements*.txt` under BASE
PREQ = os.path.join(BASE, "requirements.txt")
PREQ_DEV = os.path.join(BASE, "requirements-dev.txt")
PREQ_DEV_LIST = [line.strip() for line in open(PREQ_DEV).readlines()] if os.path.isfile(PREQ_DEV) else []
PREQ_LIST = [line.strip() for line in open(PREQ).readlines()] if os.path.isfile(PREQ) else [] + PREQ_DEV_LIST

ENTRY_POINTS = {
  'console_scripts': [
    'main = {}.main:main'.format(NAME)
  ],
  'paste.app_factory': 'main = {}:main'.format(NAME),
}

setup(
    name=NAME,
    version=BULD_VERSION,
    description=PROJECT_DESCRIPTION,
    long_description=README,
    classifiers=[
        "Codename :: {}".format(PROJECT_CODE_NAME),
        "Programming Language :: Python :: 3",
        "Topic :: {}".format(SUBJECT),
    ],
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=PROJECT_URL,
    entry_points=ENTRY_POINTS,
    packages=find_packages(),
    include_package_data=True,
    install_requires=PREQ_LIST,
    setup_requires=['pytest-runner'] + PREQ_LIST,
    tests_require=PREQ_LIST,
    test_suite=NAME,
    zip_safe=False,
)
