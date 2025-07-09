"""
Реализация DI на основе FastAPI Depends,
я бы выбрал что-то более примемлемое для ioc контейнера.
Но такая реализация Depends помогает соблюдать dependency rule
и прикладной слой с инфрой не знают про FastAPI
"""

from typing import Annotated

from fastapi import Depends

from app.application.interactors import (
    GetOrderInteractor,
    NewOrderInteractor,
    PricingPlansPaginationInteractor,
)
from app.application.services.complete_order import CompleteOrder
from app.main.ioc.infrastructure import (
    OrdersGatewayDep,
    ProviderClientADep,
    ProviderClientBDep,
    UUIDGeneratorDep,
)


# ---- Interactors ----


def get_pricing_plans_pagination_interactor(
    provider_a: ProviderClientADep,
    provider_b: ProviderClientBDep,
) -> PricingPlansPaginationInteractor:
    return PricingPlansPaginationInteractor(
        provider_a=provider_a, provider_b=provider_b
    )


PricingPlansPaginationInteractorDep = Annotated[
    PricingPlansPaginationInteractor,
    Depends(get_pricing_plans_pagination_interactor),
]


def get_new_order_interactor(
    orders_gateway: OrdersGatewayDep,
    uuid_genetator: UUIDGeneratorDep,
) -> NewOrderInteractor:
    return NewOrderInteractor(
        orders_gateway=orders_gateway,
        uuid_genetator=uuid_genetator,
    )


NewOrderInteractorDep = Annotated[
    NewOrderInteractor, Depends(get_new_order_interactor)
]


def get_order_interactor(
    orders_gateway: OrdersGatewayDep,
) -> GetOrderInteractor:
    return GetOrderInteractor(orders_gateway=orders_gateway)


GetOrderInteractorDep = Annotated[
    GetOrderInteractor, Depends(get_order_interactor)
]

# ---- Services ----


def get_complete_order(orders_gateway: OrdersGatewayDep) -> CompleteOrder:
    return CompleteOrder(orders_gateway=orders_gateway)


CompleteOrderDep = Annotated[CompleteOrder, Depends(get_complete_order)]
