from typing import Optional

from fastapi import Depends
from google.cloud.firestore import AsyncClient

from src.application.tourist_packages.repositories.tourist_packages_repository_async import \
    TouristPackagesRepositoryAsync
from src.domain.tourist_packages.entities.tourist_package import TouristPackage
from src.infrastructure.firebase.common.repositories.firestore_generic_repository_async import \
    FirestoreGenericRepositoryAsync


class FirestoreTouristPackagesRepositoryAsync(FirestoreGenericRepositoryAsync[TouristPackage, str],
                                              TouristPackagesRepositoryAsync):

    def __init__(self, firestore_client: AsyncClient = Depends(AsyncClient)):

        super().__init__(firestore_client, 'tourist_packages', TouristPackage)

    async def get_by_ref_id_async(self, ref_id: str) -> Optional[TouristPackage]:
        package_ref = self._firestore_client.collection('tourist_packages').where('ref_id', '==', ref_id).limit(1)
        user_snapshot = await package_ref.get()

        for doc in user_snapshot:
            package_data = doc.to_dict()
            package_data["id"] = doc.id
            package = TouristPackage()
            package.merge_dict(package_data)
            return package

        return None
