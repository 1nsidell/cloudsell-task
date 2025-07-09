from fastapi import APIRouter, HTTPException, Query

from app.application.common.dto.pricing_plans import PricingPlansPagination
from app.infrastructure.common.config.constants import api_prefix
from app.main.ioc import PricingPlansPaginationInteractorDep
from app.presentation.http.common.response_model import PricingPlanResponse


router = APIRouter()


@router.get(
    api_prefix.pricing_plans,
    response_model=list[PricingPlanResponse],
    status_code=200,
)
async def get_plans(
    interactor: PricingPlansPaginationInteractorDep,
    min_storage: int = Query(..., ge=1),
) -> list[PricingPlanResponse]:
    dto = PricingPlansPagination(min_storage=min_storage)
    plans = interactor.run(dto)
    if not plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    return [
        PricingPlanResponse(
            provider=plan.provider,
            storage_gb=plan.storage_gb,
            price_per_gb=plan.price_per_gb,
        )
        for plan in plans
    ]
