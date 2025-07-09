from app.application.common.dto.orders import NewOrderDTO
from app.application.common.ports.orders_gateway import OrdersGateway
from app.application.common.ports.uuid_generator import UUIDGenerator
from app.domain.entities.orders import OrderDM


class NewOrderInteractor:
    def __init__(
        self,
        orders_gateway: OrdersGateway,
        uuid_genetator: UUIDGenerator,
    ):
        self._uuid_genetator = uuid_genetator
        self._orders_gateway = orders_gateway

    def run(self, data: NewOrderDTO) -> str:
        order_id = self._uuid_genetator()
        order = OrderDM(
            order_id=order_id,
            provider=data.provider,
            storage_gb=data.storage_gb,
        )
        return self._orders_gateway.add_order(order=order)
