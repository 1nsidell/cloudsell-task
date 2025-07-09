from pydantic import BaseModel, ConfigDict
from typing_extensions import Literal


class BaseResponse(BaseModel):
    model_config = ConfigDict(strict=True)


class PricingPlanResponse(BaseResponse):
    provider: str
    storage_gb: int
    price_per_gb: float


class OrderResponse(BaseResponse):
    order_id: str
    status: Literal["pending", "complete"] = "pending"


class SuccessResponse(BaseResponse):
    message: str = "success"
