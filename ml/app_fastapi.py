"""
api_fastapi.py
"""
import fastapi
import os

from starlette.requests import Request

from ml.config import get_boolean, get_uint, settings
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)
ALL_METHODS = ['HEAD', 'GET', 'PATCH', 'PUT', 'POST', 'DELETE', 'OPTIONS']

api_host = settings('api.host')
api_path = settings('api.path')
api_port = get_uint('api.port')
api_spec_file = settings('api.spec.file')
api_spec_path = os.path.join(
    settings('api.spec.path'), settings('api.spec.version'))
api_debug = get_boolean('api.debug')

# Dev Note: somehow the `docs_url` can only serve on port 8000.
# PYTHONPATH=. uvicorn --host 0.0.0.0 --port 8000 ml.app_fastapi:app
app = fastapi.FastAPI(
    docs_url='/{}/ui'.format(api_path),
    redoc_url='/{}/docs'.format(api_path),
    openapi_url='/{}/swagger.json'.format(api_path),
    debug=api_debug)


# using `async` and `await`
#   from asgiref.sync import sync_to_async
# see https://www.aeracode.org/2018/02/19/python-async-simplified/
@app.get("/api/info", summary="Info")
def getInfo(request: Request):
    """
    Get API information.
    """
    url_host = str(request.url).replace(request.url.path, '')
    api_name = settings('api.name')
    api_desc = settings('api.desc')
    api_spec = '{}/{}/swagger.json'.format(url_host, api_path)
    api_version = settings('api.version')
    env = settings('env')

    return {
        "name": api_name,
        "version": api_version,
        "description": api_desc,
        "endpointURL": '{}/{}'.format(url_host, api_path),
        "environment": env,
        "swagger-ui": '{}{}'.format(url_host, app.docs_url),
        "spec": api_spec,
    }
