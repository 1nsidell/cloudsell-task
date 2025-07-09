import json
from pathlib import Path

from app.application.common.ports import ProviderClient
from app.domain.entities.pricing_plans import PricingPlanDM


class ProviderClientA(ProviderClient):
    """Реализация инетрфейса, для провайдера A."""

    def __init__(self, path_to_data: Path):
        self._path_to_data = path_to_data

    def get_plans(self) -> list[PricingPlanDM]:
        with open(self._path_to_data, "r") as f:
            data = json.load(f)
            return [PricingPlanDM(**item) for item in data]


class ProviderClientB(ProviderClient):
    """Реализация инетрфейса, для провайдера B."""

    def __init__(self, path_to_data: Path):
        self._path_to_data = path_to_data

    def get_plans(self) -> list[PricingPlanDM]:
        with open(self._path_to_data, "r") as f:
            data = json.load(f)
            return [PricingPlanDM(**item) for item in data]
