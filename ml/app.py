"""
ml/app.py - application entrance
using connexion to start a RESTful API service per spec defined in swagger.yaml

author: Jason Zhu <jason_zhuyx@hotmail.com>
"""
import connexion
import os

from flask import redirect
from ml.config import get_boolean, get_uint, settings
from ml.utils.logger import get_logger

api_spec_path = os.path.join(
    settings('api.spec.path'), settings('api.spec.version'))
app = connexion.App(__name__, specification_dir=api_spec_path)
LOGGER = get_logger(__name__)
SSL_CONTEXT = None  # or 'adhoc'


def main():
    """
    The main API routine.
    """
    global app

    api_host = settings('api.host')
    api_port = get_uint('api.port')
    api_spec_file = settings('api.spec.file')
    api_debug = get_boolean('api.debug')

    LOGGER.debug('loading api spec: %s/%s', api_spec_path, api_spec_file)
    app.add_api(api_spec_file)  # read from above specification_dir

    # app is a connexion application
    # app.app is a flask application; or `strict_slashes=False` on @app.route
    app.app.url_map.strict_slashes = False

    LOGGER.info('starting api server %s:%s\n', api_host, api_port)
    app.run(
        host=api_host,
        port=api_port,
        ssl_context=SSL_CONTEXT,
        debug=api_debug)


@app.route('/')
@app.route('/api')
def root():
    """
    Redirect root (/) and /api to /api/ui.
    """
    return redirect('/api/ui', code=302)


if __name__ == '__main__':
    main()
