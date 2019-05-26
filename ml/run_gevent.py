"""
run_gevent.py
"""
from gevent import monkey

# Dev Note:
# Need `monkey.patch_all()` so the wsgi server can handle concurrent requests.
# Have to patch at the top of the file here because it overrides certain python
# modules with gevent modules (e.g. threading); otherwise, it may not work.
# Not an ideal solution; probably choose a different WSGI server.
monkey.patch_all()

from gevent.pywsgi import WSGIServer  # noqa: E402
from ml.app import app  # noqa: E402
from ml.utils.logger import get_logger  # noqa: E402

LOGGER = get_logger(__name__, level='INFO')
LOGGER.info("starting wsgi server")

# configure WSGI server
http_server = WSGIServer(('localhost', 8081), app)
http_server.serve_forever()
