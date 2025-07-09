from typing import Literal

from pydantic import BaseModel, ConfigDict


class BaseRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")


class OrderCreate(BaseRequest):
    provider: Literal["A", "B"]
    storage_gb: int
