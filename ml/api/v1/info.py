"""
ml/api/v1/info.py
"""
import flask
import os

from ml.app_config import \
    api_name, api_desc, api_version, \
    api_path, \
    api_docs_url, \
    api_spec, api_spec_file, api_spec_path, \
    app_env
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


def get_api_doc():
    """
    Get API spec file, e.g. swagger.yaml.
    """
    curr_path = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.dirname(os.path.dirname(curr_path))
    spec_path = os.path.join(root_path, api_spec_path)

    LOGGER.debug('downloading %s/%s', spec_path, api_spec_file)
    res = flask.send_from_directory(
        spec_path, api_spec_file,
        as_attachment=True,
        attachment_filename='swagger-pyml.yaml',
        mimetype='application/octet-stream'
    )
    return res


def get_info():
    """
    Get API information.
    """
    base_url = flask.request.host_url.strip('/')

    return {
        "name": api_name,
        "version": api_version,
        "description": api_desc,
        "endpointURL": '{}/{}'.format(base_url, api_path),
        "environment": app_env,
        "swaggerFile": '{}/{}'.format(base_url, api_spec),
        "swaggerUi": '{}/{}'.format(base_url, api_docs_url),
    }
