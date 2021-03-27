# pylint: disable=R0915,W0612,C0415,R1702  ; complexity warnings
# NOTE: in the future, all files at this level should be moved to separate library

from typing import Any, Callable, Dict, List

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse, UJSONResponse

from conf import APP_NAME, APP_VERSION, DEBUG
from log import current_context

from .api import DEFAULT_ERROR_HEADERS, Error, InternalError


def make_app(*args: Any, **kwargs: Any) -> FastAPI:
    docs_url = '/api' if DEBUG else None
    kwargs.setdefault('docs_url', docs_url)
    kwargs.setdefault('debug', DEBUG)
    kwargs.setdefault('openapi_url', '/api/openapi.json')

    app = FastAPI(*args, **kwargs)

    set_middlewares(app)
    set_swagger(app)

    if DEBUG:  # pragma: no cover
        from starlette.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=['*'],
        )

    return app


def set_middlewares(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    def type_error_handler(request: Request, exc: RequestValidationError) -> UJSONResponse:
        return UJSONResponse(
            status_code=422,
            content={'ok': False, 'error': exc.errors()},
            headers=DEFAULT_ERROR_HEADERS,
        )

    @app.exception_handler(Error)
    def error_handler(request: Request, exc: Error) -> UJSONResponse:
        return exc.render()

    @app.exception_handler(HTTPException)
    def fastapi_error_handler(request: Request, exc: HTTPException) -> UJSONResponse:
        return UJSONResponse(
            status_code=exc.status_code,
            content={'ok': False, 'error': exc.detail},
            headers={**DEFAULT_ERROR_HEADERS, **(exc.headers or {})},
        )

    @app.middleware('http')
    async def catch_exceptions_middleware(
        request: Request, call_next: Callable[[Request], Any]
    ) -> UJSONResponse:
        try:
            return await call_next(request)
        except Exception as exc:  # pylint: disable=broad-except
            # TODO: LOG
            return InternalError(str(exc)).render()

    @app.middleware('http')
    async def log_and_trace(request: Request, call_next: Callable[[Request], Any]) -> Response:
        current_context.init()
        response: StreamingResponse = await call_next(request)
        return response


def set_swagger(app: FastAPI) -> None:
    def json_api_schema() -> Dict[Any, Any]:  # pylint: disable=R0915
        if app.openapi_schema:
            return app.openapi_schema

        SUCCESS_CODES = ('200',)
        CORRECT_SCHEMA_CODES = ('200', '422')

        openapi_schema = get_openapi(
            title=APP_NAME, version=APP_VERSION, description='OpenAPI schema', routes=app.routes,
        )

        def process_responses(responses: List[Any]) -> None:
            for response_code in responses:
                if response_code not in CORRECT_SCHEMA_CODES:
                    continue
                response = responses[response_code]
                schema = response['content']['application/json']['schema']

                new_schema = {'type': 'object'}
                if title := schema.pop('title', None):
                    new_schema['title'] = title
                new_schema['properties'] = {  # type: ignore
                    'ok': {
                        'title': 'Ok',
                        'type': 'boolean',
                        'default': response_code in SUCCESS_CODES,
                    }
                }
                if len(schema) > 1:
                    data = {'title': 'Data', **schema}
                else:
                    data = schema
                if response_code in SUCCESS_CODES:
                    field = 'data'
                else:
                    field = 'error'
                    new_schema['properties']['error_code'] = {  # type: ignore
                        'title': 'Error code',
                        'type': 'string',
                        'default': 'ERROR_CODE',
                    }
                new_schema['properties'][field] = data  # type: ignore

                response['content']['application/json']['schema'] = new_schema

        paths = openapi_schema['paths']
        for path in paths.values():
            for method in path.values():
                if tags := method.get('tags'):
                    if 'api' in tags and len(tags) > 1:
                        tags.remove('api')
                    process_responses(method['responses'])

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    setattr(app, 'openapi', json_api_schema)
