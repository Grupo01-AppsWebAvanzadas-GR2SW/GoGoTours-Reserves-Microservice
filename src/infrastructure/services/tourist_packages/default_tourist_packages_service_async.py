from datetime import datetime

from fastapi import Depends

from src.domain.tourist_packages.entities.tourist_package import TouristPackage
from src.application.tourist_packages.services.tourist_packages_service_async import TouristPackagesServiceAsync
from src.application.tourist_packages.dtos.tourist_packages_response_dto import TouristPackagesResponseDto
from src.application.tourist_packages.repositories.tourist_packages_repository_async import \
    TouristPackagesRepositoryAsync
from injector import inject


class DefaultTouristPackagesServiceAsync(TouristPackagesServiceAsync):
    def __init__(self, tourist_packages_repository_async: TouristPackagesRepositoryAsync = Depends(TouristPackagesRepositoryAsync)):
        self._tourist_packages_repository_async = tourist_packages_repository_async

    async def add_package(self, tourist_package: TouristPackagesResponseDto):
        await self._tourist_packages_repository_async.add_async(
            TouristPackage(
                ref_id=tourist_package.ref_id
            )
        )

    async def delete_package(self, ref_id: str):
        package = await self._tourist_packages_repository_async.get_by_ref_id_async(ref_id)

        if package is not None:
            await self._tourist_packages_repository_async.delete_by_id_async(package.id)
            return True
        else:
            return False
