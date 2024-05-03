from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

from shop.core.products import Product
from shop.core.receipt_product import ReceiptProduct


class ReceiptRepository(Protocol):
    def create(self, receipt: Receipt) -> None:
        pass

    def add_product(
        self, receipt: Receipt, product: Product, product_quantity: int
    ) -> None:
        pass

    def read(self, receipt_id: UUID) -> Receipt:
        pass

    def close(self, receipt_id: UUID, status: str) -> None:
        pass

    def delete(self, receipt_id: UUID) -> None:
        pass


@dataclass
class Receipt:
    status: str = "open"
    products: list[ReceiptProduct] = field(default_factory=list)
    total: float = 0.0

    id: UUID = field(default_factory=uuid4)
