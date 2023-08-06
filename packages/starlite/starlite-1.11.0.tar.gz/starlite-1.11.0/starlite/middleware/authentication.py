from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Union

from pydantic import BaseModel
from starlette.requests import HTTPConnection

from starlite.enums import MediaType, ScopeType
from starlite.exceptions import NotAuthorizedException, PermissionDeniedException
from starlite.response import Response
from starlite.types import MiddlewareProtocol

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Receive, Scope, Send


class AuthenticationResult(BaseModel):
    user: Any
    auth: Any = None

    class Config:
        arbitrary_types_allowed = True


class AbstractAuthenticationMiddleware(ABC, MiddlewareProtocol):
    scopes = {ScopeType.HTTP, ScopeType.WEBSOCKET}

    def __init__(self, app: "ASGIApp"):
        super().__init__(app)
        self.app = app

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        try:
            if scope["type"] in self.scopes:
                auth_result = await self.authenticate_request(HTTPConnection(scope))
                scope["user"] = auth_result.user
                scope["auth"] = auth_result.auth
            await self.app(scope, receive, send)
        except (NotAuthorizedException, PermissionDeniedException) as e:
            if scope["type"] == ScopeType.WEBSOCKET:  # pragma: no cover
                # we use a custom error code
                status_code = e.status_code + 4000
                await send({"type": "websocket.close", "code": status_code, "reason": repr(e)})
            response = self.create_error_response(exc=e)
            await response(scope, receive, send)
        return None

    @staticmethod
    def create_error_response(exc: Union[NotAuthorizedException, PermissionDeniedException]) -> Response:
        """Creates an Error response from the given exceptions, defaults to a JSON response"""
        return Response(
            media_type=MediaType.JSON,
            content={"detail": exc.detail, "extra": exc.extra},
            status_code=exc.status_code,
        )

    @abstractmethod
    async def authenticate_request(self, request: HTTPConnection) -> AuthenticationResult:  # pragma: no cover
        """
        Given a request, return an instance of AuthenticationResult
        containing a user and any relevant auth context, e.g. a JWT token.

        If authentication fails, raise an HTTPException, e.g. starlite.exceptions.NotAuthorizedException
        or starlite.exceptions.PermissionDeniedException
        """
        raise NotImplementedError("authenticate_request must be overridden by subclasses")
