from dataclasses import dataclass
from typing import Literal


@dataclass
class OrderDM:
    order_id: str
    provider: str
    storage_gb: int
    status: Literal["pending", "complete"] = "pending"

    def change_status(self, status: Literal["pending", "complete"]) -> None:
        self.status = status
