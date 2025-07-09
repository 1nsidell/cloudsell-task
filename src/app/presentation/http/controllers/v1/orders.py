from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.application.common.dto.orders import GetOrderDTO, NewOrderDTO
from app.infrastructure.common.config.constants import api_prefix
from app.main.ioc.application import (
    CompleteOrderDep,
    GetOrderInteractorDep,
    NewOrderInteractorDep,
)
from app.presentation.http.common.request_model import OrderCreate
from app.presentation.http.common.response_model import OrderResponse


router = APIRouter()


@router.post(api_prefix.orders, response_model=OrderResponse, status_code=201)
async def create_order(
    data: OrderCreate,
    background_tasks: BackgroundTasks,
    interactor: NewOrderInteractorDep,
    complete_order_service: CompleteOrderDep,
) -> OrderResponse:
    dto = NewOrderDTO(provider=data.provider, storage_gb=data.storage_gb)
    order_id = interactor.run(data=dto)
    background_tasks.add_task(complete_order_service.run, order_id)
    return OrderResponse(order_id=order_id)


@router.get(f"{api_prefix.orders}/{{order_id}}", response_model=OrderResponse)
async def get_order_status(
    order_id: str,
    interactor: GetOrderInteractorDep,
) -> OrderResponse:
    dto = GetOrderDTO(order_id=order_id)
    if order := interactor.run(data=dto):
        return OrderResponse(order_id=order.order_id, status=order.status)
    raise HTTPException(status_code=404, detail="Order not found")
