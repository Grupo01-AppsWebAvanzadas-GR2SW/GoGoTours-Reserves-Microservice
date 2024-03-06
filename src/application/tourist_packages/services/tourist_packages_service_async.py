from abc import ABC, abstractmethod
from src.application.tourist_packages.dtos.tourist_packages_response_dto import TouristPackagesResponseDto


class TouristPackagesServiceAsync(ABC):
    @abstractmethod
    async def add_package(self, tourist_package: TouristPackagesResponseDto):
        pass

    @abstractmethod
    async def delete_package(self, ref_id: str):
        pass
