from typing import Dict
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from shop.core.errors import DoesNotExistError, ExistsError
from shop.core.units import Unit
from shop.infra.fastapi.dependables import UnitRepositoryDependable

unit_api = APIRouter(tags=["Units"])


class CreateUnitRequest(BaseModel):
    name: str


class UnitItem(BaseModel):
    id: UUID
    name: str


class UnitEnvelope(BaseModel):
    unit: UnitItem


class UnitListEnvelope(BaseModel):
    units: list[UnitItem]


@unit_api.post("/units", status_code=201, response_model=UnitEnvelope)
def create_unit(
    request: CreateUnitRequest, units: UnitRepositoryDependable
) -> dict[str, Unit] | JSONResponse:
    unit = Unit(**request.model_dump())
    try:
        units.create(unit)
        return {"unit": unit}
    except ExistsError:
        error_message = f"Unit with name<{unit.name}> already exists."
        return JSONResponse(
            status_code=409, content={"error": {"message": error_message}}
        )


@unit_api.get(
    "/units/{unit_id}",
    status_code=200,
    response_model=UnitItem,
)
def read_unit(unit_id: UUID, units: UnitRepositoryDependable) -> Unit | JSONResponse:
    try:
        return units.read(unit_id)
    except DoesNotExistError:
        return JSONResponse(
            status_code=404,
            content={"message": f"Unit with id<{unit_id}> does not exist."},
        )


@unit_api.get("/units", response_model=UnitListEnvelope)
def read_all(units: UnitRepositoryDependable) -> Dict[str, list[Unit]] | JSONResponse:
    return {"units": units.read_all()}
