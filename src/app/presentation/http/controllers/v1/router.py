from fastapi import APIRouter

from app.infrastructure.common.config.constants import api_prefix
from app.presentation.http.controllers.v1.orders import router as orders_router
from app.presentation.http.controllers.v1.pricing_plans import (
    router as pricing_plans_router,
)


v1_router = APIRouter(
    prefix=api_prefix.v1_prefix,
    tags=["V1"],
)

v1_sub_routers = (
    orders_router,
    pricing_plans_router,
)

for router in v1_sub_routers:
    v1_router.include_router(router)
