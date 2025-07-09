"""
Реализация DI на основе FastAPI Depends,
я бы выбрал что-то более примемлемое для ioc контейнера.
Но такая реализация Depends помогает соблюдать dependency rule
и прикладной слой с инфрой не знают про FastAPI
"""

from typing import Annotated

from fastapi import Depends
import redis.asyncio as redis

from app.application.common.ports import (
    OrdersGateway,
    ProviderClient,
    UUIDGenerator,
)
from app.infrastructure.adapters import (
    OrdersGatewayImpl,
    ProviderClientA,
    ProviderClientB,
    UUIDGeneratorImpl,
)
from app.infrastructure.common.external.redis import RedisConnectionManager
from app.main.ioc.settings import ProviderADataDep, ProviderBDataDep, configs


# ---- External API ----
def get_provider_client_a(path_to_data: ProviderADataDep) -> ProviderClient:
    return ProviderClientA(path_to_data=path_to_data)


def get_provider_client_b(path_to_data: ProviderBDataDep) -> ProviderClient:
    return ProviderClientB(path_to_data=path_to_data)


ProviderClientADep = Annotated[ProviderClient, Depends(get_provider_client_a)]
ProviderClientBDep = Annotated[ProviderClient, Depends(get_provider_client_b)]


# ---- Gateway ----

# используем синглтон, чтобы объект не пересоздавался на каждый API-запрос из-за Depends
gateway = OrdersGatewayImpl()


def get_orders_gateway() -> OrdersGateway:
    return gateway


OrdersGatewayDep = Annotated[OrdersGateway, Depends(get_orders_gateway)]


RedisManager = RedisConnectionManager(configs.redis)


def get_redis_conn() -> redis.Redis:
    return RedisManager.get_connection()


RedisConnDep = Annotated[redis.Redis, Depends(get_redis_conn)]

# ---- Вспомогательный утилиты ----


def get_uuid_generator() -> UUIDGenerator:
    return UUIDGeneratorImpl()


UUIDGeneratorDep = Annotated[UUIDGenerator, Depends(get_uuid_generator)]
