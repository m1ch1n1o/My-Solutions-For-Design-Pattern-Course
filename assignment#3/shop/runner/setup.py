import os

from fastapi import FastAPI

from shop.infra.DAO.products_DAO import ProductDAO
from shop.infra.DAO.receipts_DAO import ReceiptDAO
from shop.infra.DAO.sales_DAO import SalesDAO
from shop.infra.DAO.units_DAO import UnitDAO
from shop.infra.fastapi import product_api, receipt_api, sales_api, unit_api
from shop.infra.in_memory import (
    ProductInMemory,
    ReceiptInMemory,
    SalesInMemory,
    UnitInMemory,
)


# PYTHONUNBUFFERED=1;PRODUCT_REPOSITORY_KIND=sqlite
def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(product_api)
    app.include_router(unit_api)
    app.include_router(receipt_api)
    app.include_router(sales_api)

    if os.getenv("PRODUCT_REPOSITORY_KIND", "memory") == "sqlite":
        app.state.products = ProductDAO()
        app.state.units = UnitDAO()
        app.state.receipts = ReceiptDAO()
        app.state.sales = SalesDAO()
    else:
        app.state.products = ProductInMemory()
        app.state.units = UnitInMemory()
        app.state.receipts = ReceiptInMemory()
        app.state.sales = SalesInMemory()

    return app
