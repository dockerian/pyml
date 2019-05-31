"""
api/__route.py
"""
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse

from ml.app_config import \
    ALL_METHODS, \
    api_name, api_desc, api_version, \
    api_path, \
    api_docs_url, \
    api_spec, \
    app_env
from ml.api.__models import ApiSchema
from ml.utils.logger import get_logger

LOGGER = get_logger(__name__)
ROUTER = APIRouter()


# using `async` and `await`
#   from asgiref.sync import sync_to_async
# see https://www.aeracode.org/2018/02/19/python-async-simplified/
@ROUTER.get(
    "/api/info",
    response_model=ApiSchema,
    summary="Info",
    tags=["info"])
def get_info(request: Request):
    """
    Get API information.
    """
    host_url = str(request.url).replace(request.url.path, '')

    return {
        "name": api_name,
        "version": api_version,
        "description": api_desc,
        "endpointURL": '{}/{}'.format(host_url, api_path),
        "environment": app_env,
        "swaggerFile": '{}/{}'.format(host_url, api_spec),
        "swaggerUi": '{}/{}'.format(host_url, api_docs_url),
    }


@ROUTER.api_route(
    '/api/v1/{rest_path}',
    summary="api/v1 redirect",
    description="Redirect all /api/v1/* routes to /api",
    include_in_schema=False,
    methods=ALL_METHODS)
def api_v1_redirect(request: Request, rest_path: str):
    """
    Redirect /api/v1 to /api.
    """
    http_url = str(request.url).strip('/')
    host_url = http_url.replace(request.url.path, '')
    path_src = '{}/{}/v1'.format(host_url, api_path)
    path_dst = '{}/{}'.format(host_url, api_path)
    path_url = http_url.replace(path_src, path_dst, 1)
    LOGGER.debug('mapping path: %s', http_url)
    LOGGER.debug('          to: %s\n', path_url)
    # using HTTP 307 Temporary Redirect to preserve headers and body
    redirect_url = '/api/{}'.format(rest_path)
    res = RedirectResponse(
        url=redirect_url, status_code=307)
    return res


@ROUTER.get('/api')
def api_info():
    """
    Redirect /api to /api/info.
    """
    res = RedirectResponse(url='/api/info', status_code=302)
    return res


@ROUTER.get('/')
def api_root():
    """
    Redirect root (/) to /api/ui.
    """
    res = RedirectResponse(url='/api/ui', status_code=302)
    return res
