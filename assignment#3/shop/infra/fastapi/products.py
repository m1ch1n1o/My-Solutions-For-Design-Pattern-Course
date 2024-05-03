from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from shop.core.errors import DoesNotExistError, ExistsError
from shop.core.products import Product
from shop.infra.fastapi.dependables import (
    ProductRepositoryDependable,
    UnitRepositoryDependable,
)

product_api = APIRouter(tags=["Products"])


class EmptyResponse(BaseModel):
    pass


class CreateProductRequest(BaseModel):
    unit_id: UUID
    name: str
    barcode: str
    price: float


class CreatePriceRequest(BaseModel):
    price: float


class ProductItem(BaseModel):
    id: UUID
    unit_id: UUID
    name: str
    barcode: str
    price: float


class ProductEnvelope(BaseModel):
    product: ProductItem


class ProductListEnvelope(BaseModel):
    products: list[ProductItem]


@product_api.post(
    "/products",
    status_code=201,
    response_model=ProductEnvelope,
)
def create_product(
    request: CreateProductRequest,
    products: ProductRepositoryDependable,
    units: UnitRepositoryDependable,
) -> dict[str, Product] | JSONResponse:
    product = Product(**request.model_dump())
    try:
        units.read(product.unit_id)
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Unit with id<{product.unit_id}> does not exist."}
            },
        )
    try:
        products.create(product)
        return {"product": product}
    except ExistsError:
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "message": f"Product with barcode<{product.barcode}> "
                    f"already exists."
                }
            },
        )


@product_api.patch(
    "/products/{product_id}",
    status_code=200,
    response_model=EmptyResponse,
)
def update_product(
    product_id: UUID, request: CreatePriceRequest, products: ProductRepositoryDependable
) -> EmptyResponse | JSONResponse:
    price_data = request.model_dump()
    try:
        products.update_price(product_id, price_data["price"])
        return EmptyResponse()
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Product with id<{product_id}> does not exist."}
            },
        )


@product_api.get(
    "/products/{product_id}",
    status_code=200,
    response_model=ProductItem,
)
def read_product(
    product_id: UUID, products: ProductRepositoryDependable
) -> Product | JSONResponse:
    try:
        return products.read(product_id)
    except DoesNotExistError:
        error_message = f"Product with id<{product_id}> does not exist."
        return JSONResponse(
            status_code=404,
            content={"error": {"message": error_message}},
        )


@product_api.get("/products", response_model=ProductListEnvelope)
def read_all(products: ProductRepositoryDependable) -> dict[str, list[Product]]:
    return {"products": products.read_all()}
