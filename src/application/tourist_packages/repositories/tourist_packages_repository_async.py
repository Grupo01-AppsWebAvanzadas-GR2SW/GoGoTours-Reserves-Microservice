from abc import ABC, abstractmethod
from typing import Optional

from src.domain.tourist_packages.entities.tourist_package import TouristPackage
from src.application.common.repositories.generic_repository_async import GenericRepositoryAsync, ID


class TouristPackagesRepositoryAsync(GenericRepositoryAsync[TouristPackage, str], ABC):
    @abstractmethod
    async def get_by_ref_id_async(self, ref_id: str) -> Optional[TouristPackage]:
        pass
