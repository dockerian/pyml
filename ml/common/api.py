"""
# common/api.py - generic urllib wrapper

# author: jason_zhuyx@hotmail.com
# date: 2019-01-28
"""
import json
import logging
import traceback
import urllib.request
import urllib.parse

from ml.config import get_uint
from ml.utils.logger import get_logger

DEBUG_LEVEL = DEBUG_LEVEL = get_uint('debug.level', logging.INFO)
LOGGER = get_logger(__name__, level=DEBUG_LEVEL)


def build_api_url(base_url, function, **kwargs):
    """
    @param base_url: api base URL.
    @param function: api function that will be appened to base URL with '/'.
    @param kwargs: a directory of request parameters.
    @return: an api URL, possible with encoded query string paramters.
    """
    params = check_params(kwargs)
    api_qsp = urllib.parse.urlencode(params) if params else ''
    api_url = base_url
    api_url = '{}/{}'.format(base_url, function) if function else api_url
    api_url = '{}?{}'.format(api_url, api_qsp) if api_qsp else api_url
    return api_url


def build_filter_value(filters, filter_op='and'):
    """
    @param filters: a dictionary of filter keys and values.
    @param filter_op: operator to join filters; default is 'and'.
    @return: a string represents _filter query string.
    """
    result = ''
    if isinstance(filters, dict):
        for key, value in filters.items():
            if result:
                result += ' {} '.format(filter_op)
            result += '{} == "{}"'.format(key, value)
    return result


def check_params(params):
    """
    @param params: a directory of request parameters.
    @return: a dictionary of validated request parameters.
    """
    result = {key: val for key, val in params.items() if val}
    return result


def get_api_data(api_url, api_headers={}, api_data=None):
    """
    @param api_url: a string represent full api URL.
    @param api_headers: a directory of request headers.
    @param api_data: a JSON data for POST request.
    @return: (<api data object>, <status>).
    """
    _status = None
    api_obj = None
    api_req = urllib.request.Request(api_url, headers=api_headers, data=api_data)
    # from ml.utils.extension import pickle_to_str
    request = api_req.__dict__  # pickle_to_str(api_req)
    try:
        with urllib.request.urlopen(api_req) as res:
            _status = res.status if hasattr(res, 'status') else None
            if res and res.status == 200:
                data = res.read()
                # LOGGER.debug('- response:\n%s', res.info())
                headers = res.headers
                content_type = headers.get('content-type', '').split(';')[0]
                decoded_data = data.decode('utf-8', errors='ignore')
                # LOGGER.info('- decoded data: %s', decoded_data)
                if 'application/json' in content_type:
                    api_obj = json.loads(decoded_data)
                else:
                    api_obj = {'data': decoded_data}
            elif not res:
                LOGGER.error('- unable to open api request: {}'.format(request))
            else:
                LOGGER.debug('- response:\n%s', res.info())
                LOGGER.error('- status: %s, request: %s', res.status, request)
    except Exception:
        message = 'unable to read data from request'
        LOGGER.error('- %s: %s', message, request)
        # import sys
        # exc_info = '{}: {}'.format(type(ex).__name__, ex)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # traceback.print_stack()
        traceback.print_exc()

    return api_obj, _status
