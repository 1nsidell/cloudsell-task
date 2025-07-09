from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PricingPlanDM:
    provider: str
    storage_gb: int
    price_per_gb: float
