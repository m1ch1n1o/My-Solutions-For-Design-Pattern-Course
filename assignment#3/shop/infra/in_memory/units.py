from dataclasses import dataclass, field
from uuid import UUID

from shop.core.errors import DoesNotExistError, ExistsError
from shop.core.units import Unit


@dataclass
class UnitInMemory:
    units: dict[UUID, Unit] = field(default_factory=dict)

    def create(self, unit: Unit) -> None:
        if not self.does_unit_name_exist(unit.name):
            self.units[unit.id] = unit
        else:
            raise ExistsError(unit.name)

    def does_unit_name_exist(self, name: str) -> bool:
        return any(unit.name == name for unit in self.units.values())

    def read(self, unit_id: UUID) -> Unit:
        try:
            return self.units[unit_id]
        except KeyError:
            raise DoesNotExistError(unit_id)

    def read_all(self) -> list[Unit]:
        return list(self.units.values())
