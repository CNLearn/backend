from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import CNLearnWithMessage


async def cnlearn_exception_handler(request: Request, exc: CNLearnWithMessage) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
