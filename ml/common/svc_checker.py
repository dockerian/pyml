"""
# ml.common.svc_checker.py

@author: Jason Zhu
@email: jason_zhuyx@hotmail.com
@created: 2019-01-30

"""
import copy
import logging
import re
import threading
import time

from queue import Queue
from urllib.parse import urlparse

from ml.config import get_uint
from ml.common.api import get_api_data
from ml.utils.extension import get_attr
from ml.utils.logger import get_logger

DEBUG_LEVEL = get_uint('debug.level', logging.INFO)
LOGGER = get_logger(__name__, level=DEBUG_LEVEL)

LEVEL_LIMIT = get_uint('tasks.max_nested_level', 3)


class ServiceChecker:
    """
    ServiceChecker processes a list of endpoints.
    """
    def __init__(self, endpoints, max_level=LEVEL_LIMIT):
        """
        Constructor of ml.common.ServiceChecker

        @param endpoints: a list of endpoints with recursive multi-layer
                          routes that describes app and services.
        @param max_level: the maximum nested routes level.
        @notes:
          * example of endpoints:

            ```
            [{
              "name": "endpoint 1",
              "desc": "application foobar v1.",
              "path": "http://foobar/v1",
              "format": "html",
              "routes": [{
                "name": "endpoint 1-0",
                "desc": "app service foobar api-v1.0.",
                "path": "/api/v1.0"
              }]
            }]
            ```
          * nested routes level is up to self.max_level
        """
        self._endpoints = endpoints or []
        self._max_level = LEVEL_LIMIT if max_level < 0 or max_level > LEVEL_LIMIT else max_level

        self._run_level = -1
        self._run_queue = Queue()
        self._py_locker = threading.Lock()

        self._all_paths = []  # validated endpoints
        self._templates = {
            "failure": [],
            "success": [],
        }
        self._results = copy.deepcopy(self._templates)
        self._done = False
        self._elapsed = 0
        self._start = time.time()
        self._end = self._start
        pass

    def _check_all(self, multi_threads=False):
        """
        Check all validated endpoints.
        """
        self._start = time.time()

        if not multi_threads:
            for endpoint in self._all_paths:
                self._check_endpoint(endpoint)
        else:
            self._check_all_concurrent()

        self._end = time.time()
        self._elapsed = self._end - self._start
        _tdiff = '{0:.5f}'.format(self._elapsed)
        LOGGER.info(
            'Execution time: %s [multi_threads=%s]',
            _tdiff, multi_threads)
        pass

    def _check_all_concurrent(self):
        """
        Check all validated endpoints concurrently.
        """
        for endpoint in self._all_paths:
            self._run_queue.put(endpoint)

        for endpoint in self._all_paths:
            _new_thd = threading.Thread(target=self._check_all_concurrent_queue)
            _new_thd.daemon = True
            _new_thd.start()

        self._run_queue.join()
        pass

    def _check_all_concurrent_queue(self):
        """
        Check concurrent queue, get each endpoint until it is empty.
        """
        while not self._run_queue.empty():
            endpoint = self._run_queue.get()
            self._check_endpoint(endpoint)
            self._run_queue.task_done()

    def _check_endpoint(self, endpoint):
        """
        Check single endpoint (thread-safe).
        """
        _name = endpoint.get('name')
        _path = endpoint.get('path')

        with self._py_locker:
            LOGGER.debug('* checking endpoint: %s [%s]', _name, _path)

        result, status = get_api_data(_path)

        with self._py_locker:
            self._check_endpoint_result(_path, result, status, **endpoint)

    def _check_endpoint_result(self, url, result, status, **kwargs):
        """
        Use endpoint data (kwargs) to check availability of specific url.

        @param url: the endpoint URL (str) to check.
        @param kwargs: endpoint configuration (dict).
        @return: None if success; otherwise, an error message (str).
        """
        _err = self._check_endpoint_result_(url, result, status, **kwargs)
        _msg = '* complete endpoint: {}'.format(_err or 'success')
        LOGGER.debug(_msg)
        data = self._copy_endpoint(kwargs, _err)
        results = self._results['failure'] if _err else self._results['success']
        results.append(data)

    def _check_endpoint_result_(self, url, result, status, **kwargs):
        if not result:
            return 'no response data from URL: {}'.format(url)

        _keys = kwargs.get('keys', [])
        _regx = kwargs.get('regx', '')
        _format = kwargs.get('format', 'json')
        _status = kwargs.get('status', 200)

        log = 'status={}, format={}, keys={}, regx={}, type(result)={}, url={}'.format(
            _status, _format, _keys, _regx, type(result), url)

        if not status == _status:
            return 'response status `{}` is not expected [{}] from: {}'.format(
                status, _status, url)

        if _format == 'html' and _regx:
            _regexp = re.compile(str(_regx))
            LOGGER.debug('- searching %s in response data from: %s', _regx, url)
            if not _regexp.search(str(result)):
                return 'cannot find `{}` in response data from: {}'.format(_regx, url)
            return None

        if _format != 'json' or not isinstance(result, dict) or not _keys:
            LOGGER.debug('* passed checking: %s', log)
            # no error if no additional keys to check.
            return None

        if not isinstance(_keys, list):
            _keys = [_keys]

        for key in _keys:
            value = get_attr(result, key)
            LOGGER.debug('- result[%s] = %s', key, value)
            if not value:
                return 'missing value by key `{}` in response data from: {}'.format(key, url)
        return None

    def _check_endpoint_parse(self, url):
        """
        Check if an endpoint URL is valid.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def _check_endpoint_url(self, endpoint, parent_path=''):
        """
        Check if a service endpoint is up and live.
        """
        _base = str(parent_path).strip('/')
        _path = endpoint.get('path', '').strip('/')
        _desc = endpoint.get('desc', '__unknown_service__')
        _name = endpoint.get('name', '__unnamed__')

        log_prefix = '{}- [{}]'.format('-' * self._run_level, self._run_level)
        log = 'validating endpoint URL: {} - {}'.format(_name, _desc)
        LOGGER.debug('%s %s', log_prefix, log)

        _chk1 = self._check_endpoint_parse(_path)
        _url2 = '{}/{}'.format(_base, _path) if _base else _path
        _chk2 = self._check_endpoint_parse(_url2) if not _chk1 else _chk1
        _endp = _path if _chk1 else _url2

        _data = {
            "name": _name,
            "path": _path,
        }
        if not _chk1 and not _chk2:
            _data.update({"base": _base})
            return _data, 'invalid endpoint URL: {}'.format(_path)

        _data.update(endpoint)
        _data.update({"path": _endp})
        log = 'validating endpoint URL: {}'.format('success')
        LOGGER.debug('%s %s', log_prefix, log)
        return _data, None

    def _check_service(self, endpoint, parent_path=''):
        """
        Check specific endpoint.
        """
        _data, _err = self._check_endpoint_url(endpoint, parent_path)

        if _err:
            _data.update({"_err": _err})
            self._results['failure'].append(_data)
        else:
            self._all_paths.append(_data)

        _path = _data.get('path', '')
        _name = _data.get('name', '__unnamed__')
        _next_routes = endpoint.get('routes', [])

        if _next_routes:
            if self._run_level >= self._max_level:
                err = 'cannot check routes beyond maximum nested level'
                msg = '{}: {}'.format(err, self._max_level)
                LOGGER.warning(
                    '%s* [%s] %s', '*'*self._run_level, self._run_level, msg)
                return

            log = 'checking routes for endpoint: {}'.format(_name)
            LOGGER.debug('%s- [%s] %s', '-' * self._run_level, self._run_level, log)
            self._check_services(_next_routes, _path)
        pass

    def _check_services(self, endpoints, parent_path=''):
        """
        Check a service endpoints list.
        """
        self._run_level += 1

        for svc in endpoints:
            self._check_service(svc, parent_path)

        self._run_level -= 1
        pass

    def _copy_endpoint(self, endpoint, err=None):
        """
        Make a copy of the endpoint without some keys.
        """
        data = {
            "name": endpoint.get('name'),
            "path": endpoint.get('path'),
        }
        if err:
            data['_err'] = err
        return data

    def start(self, endpoints=[], multi_threads=False):
        """
        Start to check endpoints.
        @param endpoints: new endpoints to process.
        """
        if endpoints and isinstance(endpoints, list):
            self._endpoints = endpoints  # overwrite and start with new endpoints
            self._done = False
        if isinstance(self._endpoints, list) and not self._done:
            self._all_paths = []
            self._results = copy.deepcopy(self._templates)
            self._check_services(self._endpoints)
            self._check_all(multi_threads)

        # self._done = True  # prevent from processing the endpoints again
        # returning processed results
        return self._results
