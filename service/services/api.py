# NOTE: in the future, all files at this level should be moved to separate library
# pylint: disable=too-many-lines

from enum import Enum
from inspect import Parameter, signature
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from starlette.responses import UJSONResponse

from log import current_context, log

from .schemas import ErrorResponse

DEFAULT_ERROR_HEADERS: Dict[str, str] = {}


class Api(APIRouter):
    def api_route(self, *args: Any, **kwargs: Any) -> Callable[..., Any]:  # pylint: disable=W0221
        kwargs.setdefault('response_class', APIResponse)
        return super().api_route(*args, **kwargs)


class APIResponse(UJSONResponse):
    def render(self, content: Any) -> bytes:
        if content is None:
            return super().render({'ok': True})

        if isinstance(content, dict) and 'ok' in content:
            return super().render(content)

        return super().render({'ok': True, 'data': content})


class Error(HTTPException):
    error: Optional[Union[str, Dict, List]] = None
    status_code: int = 400
    error_code: str = 'Error'
    headers: Optional[Dict[str, str]] = None

    def __init__(self, *args: Any, **kwargs: Any):
        if self.error is None:
            if len(args) == 1:
                self.error = args[0]
            else:
                raise ValueError('Only one positional arg is accepted - error message')

            self.status_code = kwargs.get('status_code', self.status_code)
            self.error_code = kwargs.get('error_code', self.error_code)

            if self.error is None:
                raise ValueError(
                    'Provide only error message or set default error template in error class to use arguments'
                )
        else:
            self.error = self.error.format(*args, **kwargs)  # type: ignore
        super().__init__(status_code=self.status_code, detail=self.error, headers=self.headers)

    def render(self) -> UJSONResponse:
        return UJSONResponse(
            status_code=self.status_code,
            content=ErrorResponse(error=self.error, error_code=self.error_code).dict(),
            headers={**DEFAULT_ERROR_HEADERS, **(self.headers or {})},
        )


class UnauthorizedError(Error):
    status_code = 401
    error_code = 'UNAUTHORIZED'


class PermissionsError(Error):
    status_code = 403
    error_code = 'INVALID_PERMISSIONS'


class NotFoundError(Error):
    status_code = 404
    error_code = 'NOT_FOUND'


class InternalError(Error):
    status_code = 500
    error_code = 'INTERNAL_SERVER_ERROR'


class ResponsesContainer(dict):
    default_responses = {
        400: {'model': ErrorResponse, 'description': 'General error'},
    }

    permissions_error = (
        403,
        {
            'model': ErrorResponse,
            'description': 'User does not have permissions to perform this action',
        },
    )
    not_found_error = (
        404,
        {'model': ErrorResponse, 'description': 'Requested resource was not found'},
    )

    errors_dict = {'permissions': permissions_error, 'not_found': not_found_error}

    def __init__(self) -> None:
        dict.__init__(self, self.default_responses)

    def __call__(self, extra: Optional[Union[str, List[str]]] = None) -> Dict[int, Dict]:
        result_responses = self.default_responses.copy()
        # it is covered, cov just does not see it for some reason
        if extra:  # pragma: no cover
            if isinstance(extra, str):
                extra = [extra]
            for key in extra:
                response = self.errors_dict.get(key)
                if not response:
                    continue
                result_responses[response[0]] = response[1]
        return result_responses


# basic usage: `@api.post(..., responses=responses)`. Error response 400 with ErrorResponse model is added by default
# `@api.post(..., responses=responses('not_found'))` - will add 404 code to default reponses
# You can add new responses to the ResponsesContainer above
responses = ResponsesContainer()
