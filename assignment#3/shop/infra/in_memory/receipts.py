from dataclasses import dataclass, field
from uuid import UUID

from shop.core.errors import ClosedError, DoesNotExistError
from shop.core.products import Product
from shop.core.receipt_product import ReceiptProduct
from shop.core.receipts import Receipt


@dataclass
class ReceiptInMemory:
    receipts: dict[UUID, Receipt] = field(default_factory=dict)

    def create(self, receipt: Receipt) -> None:
        self.receipts[receipt.id] = receipt

    def add_product(
        self, receipt: Receipt, product: Product, product_quantity: int
    ) -> None:
        receipt_product = ReceiptProduct(
            quantity=product_quantity,
            price=product.price,
            total=product_quantity * product.price,
        )
        try:
            receipt = self.receipts[receipt.id]
            receipt.products.append(receipt_product)
            receipt.total += receipt_product.total
        except KeyError:
            raise DoesNotExistError(receipt.id)

    def read(self, receipt_id: UUID) -> Receipt:
        try:
            return self.receipts[receipt_id]
        except KeyError:
            raise DoesNotExistError(receipt_id)

    def close(self, receipt_id: UUID, receipt_status: str) -> None:
        try:
            receipt = self.receipts[receipt_id]
            receipt.status = receipt_status
        except KeyError:
            raise DoesNotExistError(receipt_id)

    def delete(self, receipt_id: UUID) -> None:
        receipt = self.receipts.get(receipt_id)
        if receipt:
            if receipt.status == "closed":
                raise ClosedError(receipt_id)
            else:
                del self.receipts[receipt_id]
        else:
            raise DoesNotExistError(receipt_id)
