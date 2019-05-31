"""
app_config.py
"""
import logging
import os

from ml.config import get_boolean, get_uint, settings

ALL_METHODS = ['HEAD', 'GET', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS']
SSL_CONTEXT = 'adhoc'  # or None

api_name = settings('api.name', 'API Service')
api_desc = settings('api.desc', 'Python API Framework and Service')
api_version = settings('api.version', '1.0.0')

api_host = settings('api.host', '0.0.0.0')
api_port = get_uint('api.port', 8081)

api_icon_file = settings('api.spec.icon', 'favicon.ico')
api_root_path = os.path.dirname(os.path.realpath(__file__))
api_docs_path = settings('api.spec.path', 'apidoc')

# OpenAPI spec file and path (for spec-first framework, e.g. connexion)
api_spec_version = settings('api.spec.version', 'v1')
api_spec_file = settings('api.spec.file', 'swagger.yaml')
api_spec_path = os.path.join(
    settings('api.spec.path', 'apidoc'),
    api_spec_version)

# OpenAPI spec file and path (for code-first framework, e.g. fastapi)
api_path = settings('api.path', 'api')
api_docs_url = '{}/ui'.format(api_path)
api_redoc_url = '{}/docs'.format(api_path)
api_spec = '{}/swagger.json'.format(api_path)  # must be in JSON format

api_debug = get_boolean('api.debug', True)
app_env = settings('env', 'dev')

debug_level = get_uint('debug.level', logging.DEBUG)
ssl_enabled = get_boolean('api.enable_ssl')

static_path = os.path.join(
    api_root_path,
    settings('api.spec.path', 'apidoc'))
