import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from conf import settings
from middlewares import (
    add_process_time_header,
    exception_handler
)


def get_application() -> FastAPI:
    """
    Returns a FastAPI application.

    :return: FastAPI application.
    """

    os.environ.setdefault('FASTAPI_CONFIG', 'core.settings')

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        **settings.CORS_SETTINGS
    )

    app.middleware("http")(add_process_time_header)

    app.add_exception_handler(
        500,
        exception_handler
    )

    return app


app = get_application()
