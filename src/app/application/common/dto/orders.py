from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class NewOrderDTO:
    provider: str
    storage_gb: int


@dataclass(slots=True, frozen=True)
class GetOrderDTO:
    order_id: str
