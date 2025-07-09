from fastapi import APIRouter

from app.infrastructure.common.config.constants import api_prefix
from app.presentation.http.common.response_model import SuccessResponse


router = APIRouter()


@router.get(
    api_prefix.liveness,
    response_model=SuccessResponse,
    status_code=200,
)
async def get_liveness() -> SuccessResponse:
    return SuccessResponse()
