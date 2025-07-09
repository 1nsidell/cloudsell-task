from fastapi import APIRouter

from app.infrastructure.common.config.constants import api_prefix
from app.presentation.http.controllers.healthcheck.livness import (
    router as livness_router,
)
from app.presentation.http.controllers.healthcheck.readiness import (
    router as readiness_router,
)


healthcheck_router = APIRouter(
    prefix=api_prefix.healthcheck,
    tags=["HEALTH-CHECK"],
)

healthcheck_sub_routers = (
    livness_router,
    readiness_router,
)


for router in healthcheck_sub_routers:
    healthcheck_router.include_router(router)
