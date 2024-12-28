from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.config import settings
from api.routers import repos


@asynccontextmanager
async def lifespan(a: FastAPI):
    # TODO: connect to database
    yield


def get_app() -> FastAPI:
    a = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        lifespan=lifespan
    )
    a.include_router(repos.router, prefix=settings.API_PREFIX)

    return a


app = get_app()
