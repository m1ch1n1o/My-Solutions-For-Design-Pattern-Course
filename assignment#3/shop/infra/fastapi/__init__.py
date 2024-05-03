from shop.infra.fastapi.products import product_api
from shop.infra.fastapi.receipts import receipt_api
from shop.infra.fastapi.sales import sales_api
from shop.infra.fastapi.units import unit_api

__all__ = [
    "product_api",
    "unit_api",
    "receipt_api",
    "sales_api",
]
