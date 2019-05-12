"""
ml/api/v1/info.py
"""
import flask
import os

from ml.config import settings
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)


def get_api_doc():
    """
    Get API spec file, e.g. swagger.yaml.
    """
    curr_path = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.dirname(os.path.dirname(curr_path))
    spec_file = settings('api.spec.file')
    spec_path = os.path.join(
        root_path,
        settings('api.spec.path'),
        settings('api.spec.version'))

    LOGGER.debug('downloading %s/%s', spec_path, spec_file)
    res = flask.send_from_directory(
        spec_path, spec_file,
        as_attachment=True,
        attachment_filename='swagger-pyml.yaml',
        mimetype='application/octet-stream'
    )
    return res


def get_info():
    """
    Get API information.
    """
    api_name = settings('api.name')
    api_desc = settings('api.desc')
    api_path = settings('api.path')
    api_spec = '{}/swagger.json'.format(api_path)
    api_version = settings('api.version')
    env = settings('env')

    return {
        "name": api_name,
        "version": api_version,
        "description": api_desc,
        "endpointURL": api_path,
        "environment": env,
        "spec": api_spec,
    }