from typing import List
from fastapi import APIRouter, Depends

from src.application.reserves.dtos.reserves_request_dto import ReservesRequestDto
from src.application.reserves.dtos.reserves_response_dto import  ReservesResponseDto
from src.application.reserves.services.reserve_service_async import ReservesServiceAsync

reserves_router = APIRouter()


@reserves_router.post("/", response_model=ReservesRequestDto)
async def create_reserves(
        reserve: ReservesRequestDto,
        reserves_service: ReservesServiceAsync = Depends(ReservesServiceAsync)
) -> ReservesRequestDto:
    await reserves_service.create_reserve(reserve)
    return reserve
