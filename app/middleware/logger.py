import time
from uuid import uuid4

import structlog
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class AccessLogger(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, dispatch: DispatchFunction | None = None, *, logger: structlog.BoundLogger
    ) -> None:
        self.logger: structlog.BoundLogger = logger
        super().__init__(app, dispatch)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=str(uuid4()),
        )
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        method = request.method
        path = request.url.path
        port = request.url.port
        scheme = request.url.scheme
        query_params = str(request.query_params)
        path_params = request.path_params
        client_host = request.client.host if request.client is not None else ""
        client_port = request.client.port if request.client is not None else ""
        http_version = request.scope["http_version"]
        status_code = response.status_code
        url: str = path
        if request.scope.get("query_string"):
            url += f"?{request.scope['query_string'].decode('ascii')}"

        logged_dict = {
            "duration": duration,
            "url": str(request.url),
            "method": method,
            "path": path,
            "scheme": scheme,
            "port": port,
            "query_params": query_params,
            "path_params": path_params,
            "client_host": client_host,
            "client_port": client_port,
            "http_version": http_version,
            "status_code": status_code,
        }
        self.logger.info(
            f'{client_host}:{client_port} - "{method} {url} HTTP/{http_version}" {status_code}',
            request=logged_dict,
        )
        return response
