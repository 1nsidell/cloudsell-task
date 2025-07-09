import asyncio

from app.application.common.ports.orders_gateway import OrdersGateway


class CompleteOrder:
    def __init__(self, orders_gateway: OrdersGateway) -> None:
        self._orders_gateway = orders_gateway

    async def run(self, order_id: str) -> None:
        await asyncio.sleep(60)
        self._orders_gateway.update_status(order_id, "complete")
