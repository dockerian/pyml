"""
app.py - application entrance
using connexion to start a RESTful API service per spec defined in swagger.yaml

author: Jason Zhu <jason_zhuyx@hotmail.com>
"""
import connexion
import os

from flask import redirect, request
from ml.app_config import \
    api_host, api_port, \
    api_spec_file, api_spec_path, \
    api_debug
from ml.config import get_boolean, settings
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)

ALL_METHODS = ['HEAD', 'GET', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS']
SSL_CONTEXT = 'adhoc'  # or None

app = connexion.App(
    __name__,
    host=api_host,
    port=api_port,
    specification_dir=api_spec_path,
    debug=api_debug)


def main():
    """
    The main API routine.
    """
    ssl_context = check_cert()

    proto = 'https' if ssl_context else 'http'
    LOGGER.info('starting api server %s://%s:%s\n', proto, api_host, api_port)
    app.run(
        host=api_host,
        port=api_port,
        ssl_context=ssl_context,
        debug=api_debug)


def config_connexion():
    """
    Configure connexion API.
    """
    global app

    app.app.logger.handlers = LOGGER.handlers
    app.app.logger.setLevel(LOGGER.level)

    LOGGER.debug('loading api spec: %s/%s', api_spec_path, api_spec_file)
    app.add_api(api_spec_file)  # read from above specification_dir

    # app is a connexion application
    # app.app is a flask application; or `strict_slashes=False` on @app.route
    app.app.url_map.strict_slashes = False


def check_cert():
    ssl_context = SSL_CONTEXT
    ssl_enabled = get_boolean('api.enable_ssl')

    path_app = os.path.dirname(os.path.realpath(__file__))
    cert_key = os.path.join(path_app, settings('api.cert_key'))
    cert_pem = os.path.join(path_app, settings('api.cert_pem'))

    if os.path.isfile(cert_key) and os.path.isfile(cert_pem):
        LOGGER.debug('cert pem: %s', cert_pem)
        LOGGER.debug('cert key: %s', cert_key)
        ssl_context = (cert_pem, cert_key)

    if ssl_enabled and ssl_context:
        app.app.before_request(https_before_request)
        return ssl_context

    cert = ssl_context if isinstance(ssl_context, str) else '<cert>'
    LOGGER.debug('disabled SSL: %s [setting: %s]', cert, ssl_enabled)
    return None


def https_before_request():
    if request.url.startswith('http://'):
        https_url = request.url.replace('http://', 'https://', 1)
        return redirect(https_url, code=301)


@app.route('/api/v1/<path:rest_path>', methods=ALL_METHODS)
def root_api_v1(rest_path):
    """
    Redirect /api/v1 to /api.
    """
    http_url = request.url.strip('/')
    host_url = request.host_url.strip('/')
    path_src = host_url + '/api/v1'
    path_dst = host_url + '/api'
    path_url = http_url.replace(path_src, path_dst, 1)
    LOGGER.debug('mapping path: %s', http_url)
    LOGGER.debug('          to: %s\n', path_url)
    # using HTTP 307 Temporary Redirect to preserve headers and body
    return redirect('/api/{}'.format(rest_path), code=307)


@app.route('/api/')
def root_api():
    """
    Redirect /api to /api/info.
    """
    return redirect('/api/info', code=302)


@app.route('/')
def root():
    """
    Redirect root (/) to /api/ui.
    """
    return redirect('/api/ui', code=302)


# application = app.app # expose global WSGI application object

config_connexion()

if __name__ == '__main__':
    main()
    pass
