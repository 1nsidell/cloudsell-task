from abc import abstractmethod
from typing import Literal, Protocol

from app.domain.entities.orders import OrderDM


class OrdersGateway(Protocol):
    """Интерфейс для внешнего хранилища."""

    @abstractmethod
    def add_order(self, order: OrderDM) -> str: ...

    @abstractmethod
    def get_order(self, order_id: str) -> OrderDM | None: ...

    @abstractmethod
    def update_status(
        self,
        order_id: str,
        status: Literal["pending", "complete"],
    ) -> str | None: ...
