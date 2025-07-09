from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PricingPlansPagination:
    min_storage: int
