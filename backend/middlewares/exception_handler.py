from utils.string import exception_to_string
from fastapi.responses import JSONResponse


def exception_handler(request, exc):

    info = exception_to_string(exc)

    return JSONResponse(
        status_code=500,
        content={
            "code": "Internal Server Error",
            "detail": info
        }
    )
