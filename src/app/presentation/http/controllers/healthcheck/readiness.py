from fastapi import APIRouter, HTTPException
from redis.exceptions import ConnectionError

from app.infrastructure.common.config.constants import api_prefix
from app.main.ioc.infrastructure import RedisConnDep
from app.presentation.http.common.response_model import SuccessResponse


router = APIRouter()


@router.get(
    api_prefix.readiness,
    response_model=SuccessResponse,
    status_code=200,
)
async def get_readiness(redis: RedisConnDep) -> SuccessResponse:
    try:
        pong = await redis.ping()
        if pong is not True:
            raise ConnectionError()
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Redis connection error.")
    return SuccessResponse()
