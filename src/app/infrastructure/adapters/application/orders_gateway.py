from typing import Literal

from app.application.common.ports.orders_gateway import OrdersGateway
from app.domain.entities.orders import OrderDM


class OrdersGatewayImpl(OrdersGateway):
    def __init__(self) -> None:
        self._storage: dict[str, OrderDM] = {}

    def add_order(self, order: OrderDM) -> str:
        order_id = order.order_id
        self._storage[order_id] = order
        return order_id

    def get_order(self, order_id: str) -> OrderDM | None:
        return self._storage.get(order_id)

    def update_status(
        self,
        order_id: str,
        status: Literal["pending", "complete"],
    ) -> str | None:
        if order := self._storage.get(order_id):
            order.change_status(status)
            return order.order_id
        return None
