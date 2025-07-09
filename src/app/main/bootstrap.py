from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import APIRouter, FastAPI

from app.main.ioc.infrastructure import RedisManager


def create_app() -> FastAPI:

    return FastAPI(lifespan=lifespan)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    RedisManager.startup()
    yield
    await RedisManager.shutdown()


def configure_app(
    app: FastAPI,
    root_router: APIRouter,
) -> None:
    app.include_router(root_router)
