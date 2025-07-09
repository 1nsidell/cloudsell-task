from app.application.common.dto.orders import GetOrderDTO
from app.application.common.ports.orders_gateway import OrdersGateway
from app.domain.entities.orders import OrderDM


class GetOrderInteractor:
    def __init__(self, orders_gateway: OrdersGateway) -> None:
        self._orders_gateway = orders_gateway

    def run(self, data: GetOrderDTO) -> OrderDM | None:
        return self._orders_gateway.get_order(data.order_id)
