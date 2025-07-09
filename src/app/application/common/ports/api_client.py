from abc import abstractmethod
from typing import Protocol

from app.domain.entities import PricingPlanDM


class ProviderClient(Protocol):
    """Интерфейс для взаимодействия с внешними API."""

    @abstractmethod
    def get_plans(self) -> list[PricingPlanDM]: ...
