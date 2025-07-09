from app.application.common.dto.pricing_plans import PricingPlansPagination
from app.application.common.ports import ProviderClient
from app.domain.entities import PricingPlanDM


class PricingPlansPaginationInteractor:
    def __init__(self, provider_a: ProviderClient, provider_b: ProviderClient):
        self._provider_a = provider_a
        self._provider_b = provider_b

    def run(
        self,
        pagination: PricingPlansPagination,
    ) -> list[PricingPlanDM] | None:
        plans = self._provider_a.get_plans() + self._provider_b.get_plans()
        filtered = [p for p in plans if p.storage_gb >= pagination.min_storage]
        if not filtered:
            return None
        sorted_plans = sorted(
            filtered, key=lambda x: x.storage_gb * x.price_per_gb
        )
        return sorted_plans
