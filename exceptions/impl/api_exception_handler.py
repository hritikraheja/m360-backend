from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.api_exception import ApiException


async def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "UPSTREAM_ERROR",
            "message": str(exc),
            "path": request.url.path,
        },
    )
