from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


class ProductRepository(Protocol):
    def create(self, product: Product) -> None:
        pass

    def update_price(self, product_id: UUID, new_price: float) -> None:
        pass

    def read(self, product_id: UUID) -> Product:
        pass

    def read_all(self) -> list[Product]:
        pass


@dataclass
class Product:
    unit_id: UUID
    name: str
    barcode: str
    price: float

    id: UUID = field(default_factory=uuid4)
