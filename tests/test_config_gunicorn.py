"""
# test_config_connexion
"""
import logging
import unittest

import mock
import ml.config_gunicorn as config_gunicorn


class ConfigGunicornTester(unittest.TestCase):
    """
    ConfigGunicornTester includes all unit tests for ml.config_connexion module
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

    def test_config(self):
        self.assertTrue(config_gunicorn.workers >= 1)

    def test_hooks(self):
        environ = mock.MagicMock()
        new_value = mock.MagicMock()
        old_value = mock.MagicMock()
        req = mock.MagicMock()
        server = mock.MagicMock()
        worker = mock.MagicMock()
        resp = mock.MagicMock()
        config_gunicorn.nworkers_changed(server, new_value, old_value)
        config_gunicorn.on_exit(server)
        config_gunicorn.on_reload(server)
        config_gunicorn.on_starting(server)
        config_gunicorn.post_fork(server, worker)
        config_gunicorn.post_request(worker, req, environ, resp)
        config_gunicorn.post_worker_init(worker)
        config_gunicorn.pre_exec(server)
        config_gunicorn.pre_fork(server, worker)
        config_gunicorn.pre_request(worker, req)
        config_gunicorn.when_ready(server)
        config_gunicorn.worker_abort(worker)
        config_gunicorn.worker_exit(server, worker)
        config_gunicorn.worker_init(worker)
