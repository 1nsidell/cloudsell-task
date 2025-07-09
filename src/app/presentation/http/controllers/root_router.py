from fastapi import APIRouter

from app.infrastructure.common.config.constants import api_prefix
from app.presentation.http.controllers.healthcheck.router import (
    healthcheck_router,
)
from app.presentation.http.controllers.v1.router import v1_router


root_router = APIRouter(prefix=api_prefix.prefix)

root_sub_routers = (
    v1_router,
    healthcheck_router,
)

for router in root_sub_routers:
    root_router.include_router(router)
