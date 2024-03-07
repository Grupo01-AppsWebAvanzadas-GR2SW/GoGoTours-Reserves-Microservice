from typing import List
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials

from src.application.reserves.dtos.reserves_request_dto import ReservesRequestDto
from src.application.reserves.services.reserve_service_async import ReservesServiceAsync
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync
from src.webapi.access_security import access_security
from src.webapi.decorators import user_only_async

reserves_router = APIRouter()


@reserves_router.post("/", response_model=ReservesRequestDto)
@user_only_async
async def create_reserves(
        reserve: ReservesRequestDto,
        reserves_service: ReservesServiceAsync = Depends(ReservesServiceAsync),
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync),
        credentials: JwtAuthorizationCredentials = Security(access_security)
) -> ReservesRequestDto:
    reserve.id_customer = credentials.subject["user_id"]
    if not await tourist_packages_service.is_available_to_reserve(reserve.id_tourist_package):
        raise HTTPException(status_code=400, detail={"message": "The requested package is not available to reserve"})
    await reserves_service.create_reserve(reserve)
    return reserve


@reserves_router.head("/{package_id}/is-available")
async def is_available_to_reserve(
        package_id: str,
        tourist_packages_service: TouristPackagesServiceAsync = Depends(TouristPackagesServiceAsync)
):
    if not await tourist_packages_service.is_available_to_reserve(package_id):
        raise HTTPException(status_code=400, detail={"message": "The requested package is not available to reserve"})
    else:
        return {}
