from dataclasses import dataclass, field
from uuid import UUID

from shop.core.errors import DoesNotExistError, ExistsError
from shop.core.products import Product


@dataclass
class ProductInMemory:
    products: dict[UUID, Product] = field(default_factory=dict)

    def create(self, product: Product) -> None:
        if not self.does_product_barcode_exist(product.barcode):
            self.products[product.id] = product
        else:
            raise ExistsError(product.barcode)

    def does_product_barcode_exist(self, barcode: str) -> bool:
        return any(product.barcode == barcode for product in self.products.values())

    def update_price(self, product_id: UUID, new_price: float) -> None:
        try:
            product = self.products[product_id]
            product.price = new_price
        except KeyError:
            raise DoesNotExistError(product_id)

    def read(self, product_id: UUID) -> Product:
        try:
            return self.products[product_id]
        except KeyError:
            raise DoesNotExistError(product_id)

    def read_all(self) -> list[Product]:
        return list(self.products.values())
