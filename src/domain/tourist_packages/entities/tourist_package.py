from typing import Dict, Any
from src.domain.common.entities.base_entity import BaseEntity


class TouristPackage(BaseEntity[str]):

    def __init__(self, ref_id: str = '', entity_id: str = ''):
        super().__init__(entity_id)
        self._ref_id = ref_id

    @property
    def ref_id(self) -> str:
        return self._ref_id

    @ref_id.setter
    def ref_id(self, value: str):
        self._ref_id = value

    def merge_dict(self, source: Dict[str, Any]) -> None:
        super().merge_dict(source)
        self._ref_id = source["ref_id"]

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict["ref_id"] = self._ref_id
        return base_dict
