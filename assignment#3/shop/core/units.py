from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class UnitService:
    units: UnitRepository

    def filter_by_name(self, starts_with: str) -> list[Unit]:
        all_units = self.units.read_all()
        return [unit for unit in all_units if unit.name.startswith(starts_with)]


class UnitRepository(Protocol):
    def create(self, unit: Unit) -> None:
        pass

    def read(self, unit_id: UUID) -> Unit:
        pass

    def read_all(self) -> list[Unit]:
        pass


@dataclass
class Unit:
    name: str

    id: UUID = field(default_factory=uuid4)
