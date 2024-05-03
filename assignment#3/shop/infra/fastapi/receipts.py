from dataclasses import field
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from shop.core.errors import ClosedError, DoesNotExistError
from shop.core.receipt_product import ReceiptProduct
from shop.core.receipts import Receipt
from shop.core.sales import Sales
from shop.infra.fastapi.dependables import (
    ProductRepositoryDependable,
    ReceiptRepositoryDependable,
    SalesRepositoryDependable,
)

receipt_api = APIRouter(tags=["Receipts"])


class EmptyResponse(BaseModel):
    pass


class CreateCloseReceiptRequest(BaseModel):
    status: str = field(default="closed")


class CreateReceiptRequest(BaseModel):
    status: str
    products: list[ReceiptProduct]
    total: float


class CreateAddProductRequest(BaseModel):
    id: UUID
    quantity: int


class ReceiptProductItem(BaseModel):
    id: UUID
    quantity: int
    price: float
    total: float


class ReceiptItem(BaseModel):
    id: UUID
    status: str
    products: list[ReceiptProductItem]
    total: float


class ReceiptEnvelope(BaseModel):
    receipt: ReceiptItem


@receipt_api.post("/receipts", status_code=201, response_model=ReceiptEnvelope)
def create_receipt(
    receipts: ReceiptRepositoryDependable,
) -> dict[str, Receipt] | JSONResponse:
    receipt = Receipt()
    receipts.create(receipt)
    return {"receipt": receipt}


@receipt_api.post(
    "/receipts/{receipt_id}/products",
    status_code=200,
    response_model=ReceiptEnvelope,
)
def add_product_to_receipt(
    request: CreateAddProductRequest,
    receipts: ReceiptRepositoryDependable,
    receipt_id: UUID,
    products: ProductRepositoryDependable,
) -> dict[str, Receipt] | JSONResponse:
    product_data = request.model_dump()
    product_quantity = product_data["quantity"]
    product_id = product_data["id"]

    try:
        product = products.read(product_id)
    except DoesNotExistError:
        error_message = f"Product with id<{product_data['id']}> does not exist."
        return JSONResponse(
            status_code=404,
            content={"error": {"message": error_message}},
        )
    try:
        receipt = receipts.read(receipt_id)
        receipts.add_product(receipt, product, product_quantity)
        receipt = receipts.read(receipt_id)
        return {"receipt": receipt}
    except DoesNotExistError:
        error_message = f"Receipt with id<{receipt_id}> does not exist."
        return JSONResponse(
            status_code=404,
            content={"error": {"message": error_message}},
        )


@receipt_api.get(
    "/receipts/{receipt_id}",
    status_code=200,
    response_model=ReceiptEnvelope,
)
def read_receipt(
    receipts: ReceiptRepositoryDependable, receipt_id: UUID
) -> dict[str, Receipt] | JSONResponse:
    try:
        return {"receipt": receipts.read(receipt_id)}
    except DoesNotExistError:
        error_message = f"Receipt with id<{receipt_id}> does not exist."
        return JSONResponse(
            status_code=404,
            content={"error": {"message": error_message}},
        )


@receipt_api.patch(
    "/receipts/{receipt_id}", status_code=200, response_model=EmptyResponse
)
def close_receipt(
    receipt_id: UUID,
    requests: CreateCloseReceiptRequest,
    receipts: ReceiptRepositoryDependable,
    sales: SalesRepositoryDependable,
) -> EmptyResponse | JSONResponse:
    try:
        status = requests.status
        receipts.close(receipt_id, status)
        sales.update(Sales(n_receipts=1, revenue=receipts.read(receipt_id).total))
        return EmptyResponse()
    except DoesNotExistError:
        error_message = f"Receipt with id<{receipt_id}> does not exist."
        return JSONResponse(
            status_code=404,
            content={"error": {"message": error_message}},
        )


@receipt_api.delete(
    "/receipts/{receipt_id}",
    status_code=200,
    response_model=EmptyResponse,
)
def delete_receipt(
    receipt_id: UUID, receipts: ReceiptRepositoryDependable
) -> EmptyResponse | JSONResponse:
    try:
        receipts.delete(receipt_id)
        return EmptyResponse()
    except ClosedError:
        error_message = f"Receipt with id<{receipt_id}> is closed."
        return JSONResponse(
            status_code=403, content={"error": {"message": error_message}}
        )
    except DoesNotExistError:
        error_message = f"Receipt with id<{receipt_id}> does not exist."
        return JSONResponse(
            status_code=404, content={"error": {"message": error_message}}
        )
