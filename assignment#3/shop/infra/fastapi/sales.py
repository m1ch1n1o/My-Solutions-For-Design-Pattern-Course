from fastapi import APIRouter
from pydantic import BaseModel

from shop.core.sales import Sales
from shop.infra.fastapi.dependables import SalesRepositoryDependable

sales_api = APIRouter(tags=["Sales"])


class SalesItem(BaseModel):
    n_receipts: int
    revenue: float


class SalesEnvelope(BaseModel):
    sales: SalesItem


@sales_api.get(
    "/sales",
    status_code=200,
    response_model=SalesEnvelope,
)
def read_sales(sales: SalesRepositoryDependable) -> dict[str, Sales]:
    return {"sales": sales.read()}
