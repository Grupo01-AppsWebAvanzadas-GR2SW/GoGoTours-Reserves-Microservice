from typing import List
from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials

from src.application.reserves.dtos.reserves_request_dto import ReservesRequestDto
from src.application.reserves.services.reserve_service_async import ReservesServiceAsync
from src.webapi.access_security import access_security
from src.webapi.decorators import user_only_async

reserves_router = APIRouter()


@reserves_router.post("/", response_model=ReservesRequestDto)
@user_only_async
async def create_reserves(
        reserve: ReservesRequestDto,
        reserves_service: ReservesServiceAsync = Depends(ReservesServiceAsync),
        credentials: JwtAuthorizationCredentials = Security(access_security)
) -> ReservesRequestDto:
    reserve.id_customer = credentials.subject["user_id"]
    await reserves_service.create_reserve(reserve)
    return reserve
